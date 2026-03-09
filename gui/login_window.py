
import tkinter as tk
from tkinter import messagebox
import sqlite3
from gui.main_window import MainWindow


class LoginWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Expense Tracker Login")
        self.root.geometry("700x500")
        self.root.configure(bg="#6c63ff")

       
        card = tk.Frame(
            self.root,
            bg="white",
            width=420,
            height=340
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

       
        title = tk.Label(
            card,
            text="Expense Tracker",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#333"
        )
        title.pack(pady=20)

       
        tk.Label(
            card,
            text="Username",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.username = tk.Entry(
            card,
            width=35,
            font=("Arial", 12),
            bd=2
        )
        self.username.pack(pady=8)

        
        tk.Label(
            card,
            text="Password",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.password = tk.Entry(
            card,
            show="*",
            width=35,
            font=("Arial", 12),
            bd=2
        )
        self.password.pack(pady=8)

       
        login_btn = tk.Button(
            card,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#6c63ff",
            fg="white",
            width=22,
            relief="flat",
            command=self.login
        )
        login_btn.pack(pady=15)

       
        register_btn = tk.Button(
            card,
            text="Register",
            font=("Arial", 12),
            bg="#00b894",
            fg="white",
            width=22,
            relief="flat",
            command=self.open_register
        )
        register_btn.pack()

   
    def login(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (self.username.get(), self.password.get())
        )

        user = cur.fetchone()

        if user:
            self.root.destroy()

            root = tk.Tk()
            MainWindow(root, user[0])
            root.mainloop()

        else:
            messagebox.showerror("Error", "Invalid username or password")

    
    def open_register(self):

        from gui.register_window import RegisterWindow
        RegisterWindow(self.root)

