from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

# takes the password both of them choose and turns it into a real key
def derive_key(password):
    salt = b"fixedsalt123"  # same for Alice and Bob
    return PBKDF2(password, salt, dkLen=16, count=100000)

# this will encrypt whatever message gets sent
def encrypt(key, plaintext):
    iv = get_random_bytes(16) # random iv so every message looks diff
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv + ciphertext # put iv at the front so the other side can use it

# decrypts the message when it arrives
def decrypt(key, data):
    iv = data[:16] # first 16 bytes are in iv
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()
