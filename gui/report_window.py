import tkinter as tk
from tkinter import ttk
from datetime import datetime

from db.repository import (
    get_category_summary,
    get_monthly_summary
)

class ReportWindow:
    def __init__(self, master, main_window):
        self.master = master
        self.main_window = main_window
        self.user_id=main_window.user_id
        master.title("Reports & Summary")
        master.geometry("700x600")

        # -------- TITLE --------
        ttk.Label(
            master,
            text="Expense Summary Report",
            font=("Helvetica", 16, "bold")
        ).pack(pady=15)

        # -------- FILTER --------
        filter_frame = ttk.Frame(master)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Year:").grid(row=0, column=0, padx=5)
        self.year_var = tk.IntVar(value=datetime.now().year)
        ttk.Entry(filter_frame, textvariable=self.year_var, width=10).grid(row=0, column=1)

        ttk.Label(filter_frame, text="Month:").grid(row=0, column=2, padx=5)
        self.month_var = tk.IntVar(value=datetime.now().month)
        ttk.Entry(filter_frame, textvariable=self.month_var, width=10).grid(row=0, column=3)

        ttk.Button(
            filter_frame,
            text="Generate Report",
            command=self.load_report
        ).grid(row=0, column=4, padx=10)

        # -------- SUMMARY --------
        summary = ttk.LabelFrame(master, text="Monthly Summary")
        summary.pack(fill="x", padx=15, pady=10)

        self.income_label = ttk.Label(summary, text="Total Income: 0")
        self.expense_label = ttk.Label(summary, text="Total Expense: 0")
        self.balance_label = ttk.Label(summary, text="Balance: 0")

        self.income_label.pack(anchor="w", pady=3)
        self.expense_label.pack(anchor="w", pady=3)
        self.balance_label.pack(anchor="w", pady=3)

        # -------- CATEGORY TABLE --------
        table_frame = ttk.LabelFrame(master, text="Category-wise Summary")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Category", "Amount"),
            show="headings"
        )
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.column("Category", width=200)
        self.tree.column("Amount", width=120)

        self.tree.pack(fill="both", expand=True)

        # Load initial report
        self.load_report()

    # ================= LOAD REPORT =================
    def load_report(self):
        year = int(self.year_var.get())
        month = int(self.month_var.get())
        user_id = self.main_window.user_id

        #print("DEBUG REPORT:", user_id, year, month)

        # ----- MONTHLY SUMMARY -----
        income = 0
        expense = 0

        monthly_rows = get_monthly_summary(self.user_id,  year)
        for m, inc, exp in monthly_rows:
            if int(m) == month:
                income = inc or 0
                expense = exp or 0

        balance = income - expense

        self.income_label.config(text=f"Total Income: {income}")
        self.expense_label.config(text=f"Total Expense: {expense}")
        self.balance_label.config(text=f"Balance: {balance}")

        # ----- CATEGORY SUMMARY -----
        rows = get_category_summary(self.user_id, year, month)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for r in rows:
            self.tree.insert("", tk.END, values=r)