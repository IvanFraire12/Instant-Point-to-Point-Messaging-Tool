import tkinter as tk

root = tk.Tk()
root.title("Chat Window")

chat_box = tk.Text(root, height=20, width=50)
chat_box.pack()

root.mainloop()
