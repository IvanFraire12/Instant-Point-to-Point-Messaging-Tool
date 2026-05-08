import socket
import threading
import tkinter as tk
from crypto_utils import derive_key, encrypt, decrypt

message_count = 0
rotationCount = 0

# --- Networking setup ---
client = socket.socket()
client.connect(("127.0.0.1", 5003))

password = input("Enter shared password: ")
key = derive_key(password)

# --- GUI functions ---
# --- GUI functions ---
def send_message():
    global message_count, rotationCount, key

    msg = entry.get()
    entry.delete(0, tk.END)

    encrypted = encrypt(key, msg)
    client.send(encrypted)

    chat_box.insert(tk.END, f"You (plain): {msg}\n")
    chat_box.insert(tk.END, f"You (cipher): {encrypted.hex()}\n\n")

    # --- KEY UPDATE LOGIC ---
    message_count += 1
    if message_count % 20 == 0:
        rotationCount += 1
        key = derive_key(password + str(rotationCount))
        print(f"[KEY UPDATE] New key derived for rotationCount {rotationCount}")

def receive_messages():
    global message_count, rotationCount, key

    while True:
        data = client.recv(4096)
        if not data:
            break

        plaintext = decrypt(key, data)
        chat_box.insert(tk.END, f"Bob (cipher): {data.hex()}\n")
        chat_box.insert(tk.END, f"Bob (plain): {plaintext}\n\n")

        # --- KEY UPDATE LOGIC ---
        message_count += 1
        if message_count % 20 == 0:
            rotationCount += 1
            key = derive_key(password + str(rotationCount))
            print(f"[KEY UPDATE] New key derived for rotationCount {rotationCount}")

# --- GUI setup ---
root = tk.Tk()
root.title("Alice")

chat_box = tk.Text(root, height=20, width=60)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
