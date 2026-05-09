import struct
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

# sends data with a length in front so the other side knows how many bytes to read
def send_packet(sock, data):
    sock.sendall(struct.pack("!I", len(data)) + data)

# helper to make sure we read exactly n bytes from the socket
def recv_exact(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket closed during receive")
        data += chunk
    return data

# reads one full packet using the length prefix
def recv_packet(sock):
    length_data = recv_exact(sock, 4)
    length = struct.unpack("!I", length_data)[0]
    return recv_exact(sock, length)

# loads a private key from a pem file
def load_private_key(filename):
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

# loads a public key from a pem file
def load_public_key(filename):
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

# signs data using rsa + sha256
def sign_data(private_key, data):
    h = SHA256.new(data)
    return pkcs1_15.new(private_key).sign(h)

# checks a signature using rsa + sha256
def verify_signature(public_key, data, signature):
    h = SHA256.new(data)
    pkcs1_15.new(public_key).verify(h, signature)

# encrypts the session key with the other sides public key
def encrypt_session_key(public_key, session_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(session_key)

# decrypts the session key with the local private key
def decrypt_session_key(private_key, encrypted_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_key)

# server side handshake
# bob authenticates alice, alice authenticates bob, then bob sends a session key
def server_handshake(conn):
    bob_private = load_private_key("bob_private.pem")
    alice_public = load_public_key("alice_public.pem")

    # send alice a random challenge so she can prove who she is
    server_challenge = get_random_bytes(32)
    send_packet(conn, server_challenge)

    # alice signs bobs challenge and sends it back
    alice_signature = recv_packet(conn)
    verify_signature(alice_public, server_challenge, alice_signature)

    # now alice sends bob a challenge so bob can prove who he is
    client_challenge = recv_packet(conn)
    bob_signature = sign_data(bob_private, client_challenge)
    send_packet(conn, bob_signature)

    # bob generates a random aes session key
    session_key = get_random_bytes(16)

    # encrypt the session key with alices public key so only alice can read it
    encrypted_session_key = encrypt_session_key(alice_public, session_key)

    # sign the encrypted session key so alice knows it really came from bob
    session_signature = sign_data(bob_private, encrypted_session_key)

    send_packet(conn, encrypted_session_key)
    send_packet(conn, session_signature)

    return session_key

# client side handshake
# alice proves who she is, verifies bob, then receives the session key
def client_handshake(sock):
    alice_private = load_private_key("alice_private.pem")
    bob_public = load_public_key("bob_public.pem")

    # receive bobs challenge and sign it to prove this is really alice
    server_challenge = recv_packet(sock)
    alice_signature = sign_data(alice_private, server_challenge)
    send_packet(sock, alice_signature)

    # send bob a challenge so he can prove this is really bob
    client_challenge = get_random_bytes(32)
    send_packet(sock, client_challenge)

    # bob signs alices challenge and sends it back
    bob_signature = recv_packet(sock)
    verify_signature(bob_public, client_challenge, bob_signature)

    # receive the encrypted session key and bobs signature on it
    encrypted_session_key = recv_packet(sock)
    session_signature = recv_packet(sock)
    verify_signature(bob_public, encrypted_session_key, session_signature)

    # alice decrypts the session key with her private key
    session_key = decrypt_session_key(alice_private, encrypted_session_key)

    return session_key