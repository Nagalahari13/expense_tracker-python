import tkinter as tk
from tkinter import messagebox
import sqlite3


class RegisterWindow:

    def __init__(self, root):

        self.win = tk.Toplevel(root)
        self.win.title("Register")
        self.win.geometry("300x250")

        tk.Label(self.win, text="New Username").pack(pady=5)
        self.username = tk.Entry(self.win)
        self.username.pack()

        tk.Label(self.win, text="New Password").pack(pady=5)
        self.password = tk.Entry(self.win, show="*")
        self.password.pack()

        tk.Button(self.win, text="Create Account", command=self.register).pack(pady=10)

    def register(self):

        username = self.username.get()
        password = self.password.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        try:

            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )

            conn.commit()

            messagebox.showinfo("Success", "Account created successfully")

            self.win.destroy()

        except sqlite3.IntegrityError:

            messagebox.showerror("Error", "Username already exists")

        conn.close()