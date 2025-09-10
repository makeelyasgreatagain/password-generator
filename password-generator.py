import string
import random
import tkinter as tk
from tkinter import messagebox

def generate_password():
    charlist = string.ascii_letters + string.digits + string.punctuation
    password = ""

    length = int(entry_length.get())
    if length >= 8:
        for i in range(length):
            password += random.choice(charlist)
        messagebox.showinfo("Generated Password", password)
    else:
        messagebox.showerror("Low Length Error", "I can't generate shorter than 8 characters password due to security reasons.")

root = tk.Tk()
root.title = "Random Password Generator"

tk.Label(root, text="Enter password length: ").grid(row=0, column=0, padx=5, pady=10)
entry_length = tk.Entry(root)
entry_length.grid(row=0, column=1, padx=10, pady=10)

btn_generate = tk.Button(root, text="Generate Password", command=generate_password)
btn_generate.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
