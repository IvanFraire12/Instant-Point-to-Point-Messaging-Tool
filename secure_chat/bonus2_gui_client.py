import socket
import threading
import tkinter as tk
from crypto_utils import encrypt, decrypt
from bonus2_auth_utils import client_handshake

# setting up the client socket so Alice connects to Bob
client = socket.socket()
client.connect(("127.0.0.1", 5005))

# instead of using a shared password, Alice authenticates Bob and receives a session key
key = client_handshake(client)
print("[AUTH SUCCESS] Alice authenticated Bob and established a shared session key")

# this will handle sending messages from Alice to Bob
def send_message():
    global key

    # get the message from what Alice said in the text box
    msg = entry.get()
    entry.delete(0, tk.END)

    # encrypt it before sending to Bob using the negotiated session key
    encrypted = encrypt(key, msg)
    client.send(encrypted)

    # show both the plain and cipher text in Alice's chat box
    chat_box.insert(tk.END, f"You (plain): {msg}\n")
    chat_box.insert(tk.END, f"You (cipher): {encrypted.hex()}\n\n")

# listens for messages from Bob and decrypts them when they get here
def receive_messages():
    global key

    while True:
        data = client.recv(4096)
        if not data:
            break

        # decrypt what Bob sent
        plaintext = decrypt(key, data)

        # show both the cipher and plain text in Alice's chat box
        chat_box.insert(tk.END, f"Bob (cipher): {data.hex()}\n")
        chat_box.insert(tk.END, f"Bob (plain): {plaintext}\n\n")

# basic GUI setup for Alice's window
root = tk.Tk()
root.title("Alice - Bonus 2")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

# run the receiver in the background so the GUI doesnt freeze
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()