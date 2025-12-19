import tkinter as tk
from tkinter import ttk, messagebox
from db.repository import get_all_categories, insert_budget, get_all_budgets, delete_budget, update_budget



class BudgetWindow(tk.Toplevel):
    def __init__(self, main_window, user_id):
        super().__init__(main_window.root)
        self.main_window = main_window
        self.user_id = user_id

        self.title("Manage Budgets")
        self.geometry("450x400")

        # Category dropdown
        ttk.Label(self, text="Category:").pack(anchor="w", padx=10, pady=5)
        categories = get_all_categories()
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            self,
            textvariable=self.category_var,
            values=get_all_categories(),
            state="readonly"
        )
        self.category_dropdown.pack(pady=10)

        if categories:
            self.category_dropdown.current(0)

        # Budget amount
        ttk.Label(self, text="Monthly Budget Amount:").pack(anchor="w", padx=10, pady=5)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack(fill="x", padx=10)

        ttk.Button(self, text="Save Budget", command=self.save_budget).pack(pady=10)

        # Budget list
        self.tree = ttk.Treeview(self, columns=("id", "category", "amount"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Budget Amount")
        self.tree.column("id", width=50)
        self.tree.pack(fill="both", expand=True)

        ttk.Button(self, text="Delete Selected", command=self.delete_selected).pack(pady=5)

        self.load_budgets()

    def load_budgets(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for b in get_all_budgets():
            self.tree.insert("", "end", values=b)

    def save_budget(self):
        category = self.category_dropdown.get()
        amount_text = self.amount_entry.get()

        if not category or not amount_text:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        insert_budget(category, amount, self.user_id)
        self.load_budgets()
        messagebox.showinfo("Success", "Budget saved successfully")
        print("CATEGORY:", category)
        print("AMOUNT:", amount_text)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = selected[0]
        budget_id = self.tree.item(item)["values"][0]

        delete_budget(budget_id)
        self.load_budgets()
