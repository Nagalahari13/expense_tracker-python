import tkinter as tk
from tkinter import ttk
import sqlite3
from gui.transaction_form import TransactionForm


class TransactionPage:

    def __init__(self, parent, user_id):

        self.parent = parent
        self.user_id = user_id

       
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True)

        
        title = tk.Label(
            frame,
            text="Transactions",
            font=("Arial", 22, "bold"),
            bg="white"
        )
        title.pack(pady=10)

       
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Transaction",
            bg="#6c63ff",
            fg="white",
            font=("Arial", 11, "bold"),
            width=16,
            command=self.open_add
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Edit Transaction",
            bg="#00b894",
            fg="white",
            font=("Arial", 11, "bold"),
            width=16,
            command=self.edit_transaction
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            btn_frame,
            text="Delete Transaction",
            bg="#d63031",
            fg="white",
            font=("Arial", 11, "bold"),
            width=16,
            command=self.delete_transaction
        ).grid(row=0, column=2, padx=10)

        tk.Button(
            btn_frame,
            text="Refresh",
            bg="#0984e3",
            fg="white",
            font=("Arial", 11, "bold"),
            width=16,
            command=self.load_data
        ).grid(row=0, column=3, padx=10)

        
        columns = ("id", "date", "category", "amount", "notes")

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

       
        self.load_data()

    
    def load_data(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT id, date, category, amount, notes FROM transactions WHERE user_id=?",
            (self.user_id,)
        )

        rows = cur.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    
    def open_add(self):

        TransactionForm(
            self.tree.winfo_toplevel(),
            self.user_id,
            self.load_data
        )

   
    def edit_transaction(self):

        selected = self.tree.selection()

        if not selected:
            return

        item = selected[0]
        values = self.tree.item(item)["values"]

        TransactionForm(
            self.tree.winfo_toplevel(),
            self.user_id,
            self.load_data,
            transaction=values
        )

    
    def delete_transaction(self):

        selected = self.tree.selection()

        if not selected:
            return

        item = selected[0]
        values = self.tree.item(item)["values"]

        transaction_id = values[0]

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM transactions WHERE id=?",
            (transaction_id,)
        )

        conn.commit()
        conn.close()

        self.load_data()