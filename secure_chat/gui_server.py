import socket
import threading
import tkinter as tk
from crypto_utils import derive_key, encrypt, decrypt

# --- Networking setup ---
server = socket.socket()
server.bind(("127.0.0.1", 5000))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print("Connected to:", addr)

password = input("Enter shared password: ")
key = derive_key(password)

# --- GUI functions ---
def send_message():
    msg = entry.get()
    entry.delete(0, tk.END)

    encrypted = encrypt(key, msg)
    conn.send(encrypted)

    chat_box.insert(tk.END, f"You (plain): {msg}\n")
    chat_box.insert(tk.END, f"You (cipher): {encrypted.hex()}\n\n")

def receive_messages():
    while True:
        data = conn.recv(4096)
        if not data:
            break
        plaintext = decrypt(key, data)
        chat_box.insert(tk.END, f"Alice (cipher): {data.hex()}\n")
        chat_box.insert(tk.END, f"Alice (plain): {plaintext}\n\n")

# --- GUI setup ---
root = tk.Tk()
root.title("Bob")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
