import socket

# creates client socket and connects to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5002))

from crypto_utils import derive_key, encrypt

password = input("Enter shared password: ") # asks for shared password
key = derive_key(password) # generates encryption key 

# infinite loop for client to keep sending msgs 
while True:
    msg = input("Enter message: ")
    encrypted = encrypt(key, msg) # encrypts the msg before sending
    client.send(encrypted)
