import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt


class ReportsPage:

    def __init__(self, parent, user_id):

        self.user_id = user_id

        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Expense Reports",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title.pack(pady=20)

        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Category Report",
            bg="#6c63ff",
            fg="white",
            width=20,
            command=self.category_report
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Expense Pie Chart",
            bg="#00b894",
            fg="white",
            width=20,
            command=self.pie_report
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            btn_frame,
            text="Monthly Report",
            bg="#0984e3",
            fg="white",
            width=20,
            command=self.monthly_report
        ).grid(row=0, column=2, padx=10)

   
    def category_report(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT category, SUM(amount) FROM transactions WHERE user_id=? GROUP BY category",
            (self.user_id,)
        )

        data = cur.fetchall()
        conn.close()

        if not data:
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.bar(categories, amounts)
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.show()

   
    def pie_report(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT category, SUM(amount) FROM transactions WHERE user_id=? GROUP BY category",
            (self.user_id,)
        )

        data = cur.fetchall()
        conn.close()

        if not data:
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title("Expense Distribution")
        plt.show()

 
    def monthly_report(self):

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT substr(date,1,7), SUM(amount) FROM transactions WHERE user_id=? GROUP BY substr(date,1,7)",
            (self.user_id,)
        )

        data = cur.fetchall()
        conn.close()

        if not data:
            return

        months = [row[0] for row in data]
        totals = [row[1] for row in data]

        plt.plot(months, totals, marker="o")
        plt.title("Monthly Expenses")
        plt.xlabel("Month")
        plt.ylabel("Total Expense")
        plt.show()