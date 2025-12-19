import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db.repository import insert_transaction
from db.repository import get_total_spent_by_category,get_all_budgets
from db.repository import get_all_categories

class TransactionForm(tk.Toplevel):
    def __init__(self, main_window,user_id, transaction=None):
        super().__init__(main_window.root)
        self.main_window= main_window
        self.user_id=user_id
        self.transaction = transaction
        

        self.title("Add Transaction")
        self.geometry("400x450")

        ttk.Label(self, text="Date (YYYY-MM-DD):").pack(anchor="w", padx=10, pady=5)
        self.date_entry = ttk.Entry(self)
        self.date_entry.pack(fill="x", padx=10)

        ttk.Label(self, text="Type:").pack(anchor="w", padx=10, pady=5)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self, textvariable=self.type_var, values=["income", "expense"])
        self.type_dropdown.pack(fill="x", padx=10)

        

        ttk.Label(self, text="Category:").pack(anchor="w", padx=10, pady=5)

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
        self, 
        textvariable=self.category_var,
        state="readonly"
        
        )
        categories=get_all_categories()
        self.category_dropdown["values"]=categories

        if categories:
            self.category_dropdown.current(0)
        self.category_dropdown.pack(fill="x",padx=10)

        ttk.Label(self, text="Amount:").pack(anchor="w", padx=10, pady=5)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack(fill="x", padx=10)

        ttk.Label(self, text="Payment Method:").pack(anchor="w", padx=10, pady=5)
        self.payment_entry = ttk.Entry(self)
        self.payment_entry.pack(fill="x", padx=10)

        ttk.Label(self, text="Tags:").pack(anchor="w", padx=10, pady=5)
        self.tags_entry = ttk.Entry(self)
        self.tags_entry.pack(fill="x", padx=10)

        ttk.Label(self, text="Notes:").pack(anchor="w", padx=10, pady=5)
        self.notes_entry = ttk.Entry(self)
        self.notes_entry.pack(fill="x", padx=10)

        ttk.Button(self, text="Save Transaction", command=self.save_transaction).pack(pady=20)

    def save_transaction(self):
        date = self.date_entry.get()
        type = self.type_var.get()
        category = self.category_var.get()
        amount = float(self.amount_entry.get())
        payment_method = self.payment_entry.get()
        tags = self.tags_entry.get()
        notes = self.notes_entry.get()
        budgets = get_all_budgets()
        for b in budgets:
            budget_id, budget_category,limit_amt=b
            if budget_category==category and type=="expense":
                spent = get_total_spent_by_category(category)
                if spent + amount > limit_amt:
                    messagebox.showwarning("Budget Warning",f"you will exceed the budget for {category}!")
                    return
        if self.transaction:
            from db.repository import update_transaction
            update_transaction(self.transaction[0],date,type,category,amount,payment_method,tags,notes)
        else:
            insert_transaction(
                self.user_id,
                date,
                type,
                category, 
                amount,
                payment_method,
                tags,
                notes
            )

        self.main_window.load_transactions()
        self.destroy()
    def refresh_category_dropdown(self):
        from db.repository import get_all_categories
        self.category_dropdown["values"]=get_all_categories()