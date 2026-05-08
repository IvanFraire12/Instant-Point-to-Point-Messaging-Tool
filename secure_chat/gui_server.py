import socket
import threading
import tkinter as tk
from crypto_utils import derive_key, encrypt, decrypt

message_count = 0
rotationCount = 0

# setting up the server socket so Bob can wiat for Alice to connect
server = socket.socket()
server.bind(("127.0.0.1", 5003))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print("Connected to:", addr)

# Bob and ALice choose the ssame shared password so both sides get the same key
password = input("Enter shared password: ")
key = derive_key(password)

# handles sending messages from Bob to Alice
def send_message():
    global message_count, rotationCount, key

#get whatever Bob typed in the text box
    msg = entry.get()
    entry.delete(0, tk.END)

#encrypt it before sending to Alice
    encrypted = encrypt(key, msg)
    conn.send(encrypted)

    # show both the plain and cipher text in Bob's chat box
    chat_box.insert(tk.END, f"You (plain): {msg}\n")
    chat_box.insert(tk.END, f"You (cipher): {encrypted.hex()}\n\n")

    # rotate the key every 20 messages same as alice!
    message_count += 1
    if message_count % 20 == 0:
        rotationCount += 1
        key = derive_key(password + str(rotationCount))
        print(f"[KEY UPDATE] New key derived for rotationCount {rotationCount}")

# listens for messages from Alice and decrypts them when they get them
def receive_messages():
    global message_count, rotationCount, key

    while True:
        data = conn.recv(4096)
        if not data:
            break

            # decrypt what Alice sent
        plaintext = decrypt(key, data)
        chat_box.insert(tk.END, f"Alice (cipher): {data.hex()}\n")
        chat_box.insert(tk.END, f"Alice (plain): {plaintext}\n\n")

        # samw key rotation logic as before to make sure key gets updated after 20 messages!
        message_count += 1
        if message_count % 20 == 0:
            rotationCount += 1
            key = derive_key(password + str(rotationCount))
            print(f"[KEY UPDATE] New key derived for rotationCount {rotationCount}")

# basic GUI setup for Bob's window
root = tk.Tk()
root.title("Bob")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

# run the receiver in the background so the GUI doesnt freeze
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
