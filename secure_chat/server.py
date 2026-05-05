import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5002))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print("Connected to:", addr)

from crypto_utils import derive_key, decrypt

password = input("Enter shared password: ")
key = derive_key(password)

while True:
    data = conn.recv(4096)
    if not data:
        break
    plaintext = decrypt(key, data)
    print("Received (plaintext):", plaintext)
    print("Received (ciphertext):", data.hex())

