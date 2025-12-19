import tkinter as tk
from tkinter import ttk, messagebox
from gui.main_window import MainWindow
from db.repository import authenticate_user, register_user

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        self.root.title("Login - Personal Expense Tracker")
        self.root.geometry("400x300")
        self.root.configure(bg="#f2f6ff")

        container = tk.Frame(root, bg="#f2f6ff")
        container.pack(expand=True)

        title = tk.Label(
            container,
            text="Personal Expense Tracker",
            font=("Helvetica", 16, "bold"),
            bg="#f2f6ff"
        )
        title.pack(pady=20)

        ttk.Label(container, text="Username").pack(pady=5)
        self.username = ttk.Entry(container, width=30)
        self.username.pack()

        ttk.Label(container, text="Password").pack(pady=5)
        self.password = ttk.Entry(container, width=30, show="*")
        self.password.pack()

        ttk.Button(
            container,
            text="Login",
            command=self.login
        ).pack(pady=20)

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error","Username and password required")
            return

        user = authenticate_user(username, password)

        if not user:
            register_user(username, password)
            user = authenticate_user(username, password)

        user_id = user[0]  

        for widget in self.root.winfo_children():
            widget.destroy()

        self.on_success(self.root, user_id)
        