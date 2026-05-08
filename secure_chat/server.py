import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates server socket
server.bind(("0.0.0.0", 5002)) # binds server to port 5002
server.listen(1) # listens for incoming connections

print("Waiting for connection...")
conn, addr = server.accept() # accepts the client connection
print("Connected to:", addr)

from crypto_utils import derive_key, decrypt

password = input("Enter shared password: ") # asks for shared password
key = derive_key(password) # generayes encryption key

# infinite loop for server to keep recieving msgs
while True:
    data = conn.recv(4096)
    if not data:
        break
    plaintext = decrypt(key, data)
    print("Received (plaintext):", plaintext)
    print("Received (ciphertext):", data.hex())

