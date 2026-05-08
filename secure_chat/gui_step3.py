import tkinter as tk

# sends messages when the send button is clicked
def send_message():
    msg = entry.get()                     
    chat_box.insert(tk.END, "You: " + msg + "\n") 
    entry.delete(0, tk.END)               

root = tk.Tk() # creates the main chat window
root.title("Chat Window")

chat_box = tk.Text(root, height=20, width=50) # creates txt box for chat msgs
chat_box.pack()

entry = tk.Entry(root, width=40) # creates input box where users type msgs
entry.pack(side=tk.LEFT)

send_btn = tk.Button(root, text="Send", command=send_message) # creates send button
send_btn.pack(side=tk.LEFT)

root.mainloop()

