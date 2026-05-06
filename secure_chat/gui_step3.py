import tkinter as tk

def send_message():
    msg = entry.get()                       # Get text from input box
    chat_box.insert(tk.END, "You: " + msg + "\n")  # Show it in chat area
    entry.delete(0, tk.END)                 # Clear the input box

root = tk.Tk()
root.title("Chat Window")

chat_box = tk.Text(root, height=20, width=50)
chat_box.pack()

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT)

root.mainloop()

