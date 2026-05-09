import socket
import threading
import tkinter as tk
from crypto_utils import encrypt, decrypt
from bonus2_auth_utils import server_handshake

# setting up the server socket so Bob can wait for Alice to connect
server = socket.socket()
server.bind(("127.0.0.1", 5005))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print("Connected to:", addr)

# instead of using a shared password, Bob authenticates Alice and sets up a session key
key = server_handshake(conn)
print("[AUTH SUCCESS] Bob authenticated Alice and established a shared session key")

# handles sending messages from Bob to Alice
def send_message():
    global key

    # get whatever Bob typed in the text box
    msg = entry.get()
    entry.delete(0, tk.END)

    # encrypt it before sending to Alice using the negotiated session key
    encrypted = encrypt(key, msg)
    conn.send(encrypted)

    # show both the plain and cipher text in Bob's chat box
    chat_box.insert(tk.END, f"You (plain): {msg}\n")
    chat_box.insert(tk.END, f"You (cipher): {encrypted.hex()}\n\n")

# listens for messages from Alice and decrypts them when they get here
def receive_messages():
    global key

    while True:
        data = conn.recv(4096)
        if not data:
            break

        # decrypt what Alice sent
        plaintext = decrypt(key, data)
        chat_box.insert(tk.END, f"Alice (cipher): {data.hex()}\n")
        chat_box.insert(tk.END, f"Alice (plain): {plaintext}\n\n")

# basic GUI setup for Bob's window
root = tk.Tk()
root.title("Bob - Bonus 2")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

# run the receiver in the background so the GUI doesnt freeze
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()