import tkinter as tk
import matplotlib.pyplot as plt
import sqlite3


class DashboardPage:

    def __init__(self, parent, user_id):

        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Dashboard",
            font=("Arial", 22, "bold"),
            bg="white"
        )
        title.pack(pady=20)

        button = tk.Button(
            frame,
            text="Show Expense chart",
            command=lambda: self.show_chart(user_id)
        )
        button.pack(pady=20)

    def show_chart(self, user_id):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT category, SUM(amount) FROM transactions WHERE user_id=? GROUP BY category",
            (user_id,)
        )

        data = cur.fetchall()

        categories = [x[0] for x in data]
        amounts = [x[1] for x in data]

        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.show()