import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt


class DashboardPage:

    def __init__(self, parent, user_id):

        self.user_id = user_id

        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title.pack(pady=20)

       
        stats_frame = tk.Frame(frame, bg="white")
        stats_frame.pack(pady=10)

        total = self.get_total_expense()
        count = self.get_transaction_count()

        self.create_card(stats_frame, "Total Expense", f"₹ {total}", "#6c63ff", 0)
        self.create_card(stats_frame, "Transactions", count, "#00b894", 1)

        chart_btn = tk.Button(
            frame,
            text="Show Expense Chart",
            bg="#0984e3",
            fg="white",
            width=20,
            command=self.show_chart
        )
        chart_btn.pack(pady=30)

    def create_card(self, parent, title, value, color, column):

        card = tk.Frame(parent, bg=color, width=200, height=100)
        card.grid(row=0, column=column, padx=20)

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Arial", 12),
            bg=color,
            fg="white"
        ).pack(pady=5)

        tk.Label(
            card,
            text=value,
            font=("Arial", 18, "bold"),
            bg=color,
            fg="white"
        ).pack()

   
    def get_total_expense(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id=?",
            (self.user_id,)
        )

        result = cur.fetchone()[0]

        conn.close()

        return result if result else 0

   
    def get_transaction_count(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM transactions WHERE user_id=?",
            (self.user_id,)
        )

        result = cur.fetchone()[0]

        conn.close()

        return result

   
    def show_chart(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT category, SUM(amount) FROM transactions WHERE user_id=? GROUP BY category",
            (self.user_id,)
        )

        data = cur.fetchall()

        if not data:
            return

        categories = [x[0] for x in data]
        amounts = [x[1] for x in data]

        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.show()