
import tkinter as tk
from gui.transaction_page import TransactionPage
from gui.dashboard_page import DashboardPage


class MainWindow:

    def __init__(self, root, user_id):

        self.root = root
        self.user_id = user_id

        root.title("Personal Expense Tracker")
        root.geometry("1100x650")

        
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

       
        
        sidebar = tk.Frame(container, bg="#2c3e50", width=220)
        sidebar.pack(side="left", fill="y")

        title = tk.Label(
            sidebar,
            text="Expense Tracker",
            bg="#2c3e50",
            fg="white",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)


        tk.Button(
            sidebar,
            text="🏠 Home",
            bg="#34495e",
            fg="white",
            relief="flat",
            command=self.show_home
        ).pack(fill="x", pady=5)


        tk.Button(
            sidebar,
            text="💳 Transactions",
            bg="#34495e",
            fg="white",
            relief="flat",
            command=self.show_transactions
        ).pack(fill="x", pady=5)


        tk.Button(
            sidebar,
            text="📊 Dashboard",
            bg="#34495e",
            fg="white",
            relief="flat",
            command=self.show_dashboard
        ).pack(fill="x", pady=5)


        tk.Button(
            sidebar,
            text="📁 Reports",
            bg="#34495e",
            fg="white",
            relief="flat",
            command=self.show_reports
        ).pack(fill="x", pady=5)  

        
        self.content = tk.Frame(container, bg="white")
        self.content.pack(side="left", fill="both", expand=True)

        self.show_home()

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):

        self.clear_content()

        label = tk.Label(
            self.content,
            text="Welcome to Personal Expense Tracker",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        label.pack(pady=40)

    def show_dashboard(self):

        self.clear_content()

        DashboardPage(self.content, self.user_id)

    def show_transactions(self):

        self.clear_content()

        TransactionPage(self.content, self.user_id)

    def show_reports(self):

        self.clear_content()

        from gui.reports_page import ReportsPage

        ReportsPage(self.content, self.user_id)

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

