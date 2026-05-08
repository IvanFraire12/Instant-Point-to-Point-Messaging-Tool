import socket
import threading
import tkinter as tk
from crypto_utils import derive_key, encrypt, decrypt

message_count = 0
rotationCount = 0

# setting up the client socket Alice connects to Bob!
client = socket.socket()
client.connect(("127.0.0.1", 5003))

# Alice and Bob choose the same shared password and end up with the same key
password = input("Enter shared password: ")
key = derive_key(password)

# this will handle sending messages from Alice to Bob
def send_message():
    global message_count, rotationCount, key

    # get the message from what Alice said in the text box
    msg = entry.get()
    entry.delete(0, tk.END)

    # encrypt it beofre sending to bob
    encrypted = encrypt(key, msg)
    client.send(encrypted)

    # show both the plain and cipher text in Alice's chat box
    chat_box.insert(tk.END, f"You (plain): {msg}\n")
    chat_box.insert(tk.END, f"You (cipher): {encrypted.hex()}\n\n")

    # make sure to update the key after 20 messages!!
    message_count += 1
    if message_count % 20 == 0:
        rotationCount += 1
        key = derive_key(password + str(rotationCount))
        print(f"[KEY UPDATE] New key derived for rotationCount {rotationCount}")

# listens for messages from Bob and decrypts then when  they get them
def receive_messages():
    global message_count, rotationCount, key

    while True:
        data = client.recv(4096)
        if not data:
            break

            # decrypt what Bob sent
        plaintext = decrypt(key, data)

        #show both the cipher and plain text in Alices chat box
        chat_box.insert(tk.END, f"Bob (cipher): {data.hex()}\n")
        chat_box.insert(tk.END, f"Bob (plain): {plaintext}\n\n")

        # same key rotation logive as b4 to make sure key gets updated afer 20
        message_count += 1
        if message_count % 20 == 0:
            rotationCount += 1
            key = derive_key(password + str(rotationCount))
            print(f"[KEY UPDATE] New key derived for rotationCount {rotationCount}")

# basic GUI setup for Alice's window
root = tk.Tk()
root.title("Alice")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

# run the receiver in the background so the GUI doesnt freeze
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
