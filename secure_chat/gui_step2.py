import tkinter as tk

root = tk.Tk() # creates the main chat window
root.title("Chat Window")

chat_box = tk.Text(root, height=20, width=50) # creates txt boc for chat msgs
chat_box.pack()

root.mainloop()
