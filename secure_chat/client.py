import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5002))

from crypto_utils import derive_key, encrypt

password = input("Enter shared password: ")
key = derive_key(password)

while True:
    msg = input("Enter message: ")
    encrypted = encrypt(key, msg)
    client.send(encrypted)
