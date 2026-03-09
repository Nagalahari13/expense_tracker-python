import tkinter as tk
import sqlite3


class TransactionForm:

    def __init__(self, parent, user_id, refresh_callback, transaction=None):

        self.user_id = user_id
        self.refresh_callback = refresh_callback
        self.transaction = transaction

        
        self.win = tk.Toplevel(parent)
        self.win.title("Transaction Form")
        self.win.geometry("400x300")

       
        self.win.update_idletasks()
        x = (self.win.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.win.winfo_screenheight() // 2) - (300 // 2)
        self.win.geometry(f"+{x}+{y}")

        
        tk.Label(self.win, text="Date").pack(pady=5)
        self.date = tk.Entry(self.win)
        self.date.pack()

        
        tk.Label(self.win, text="Category").pack(pady=5)
        self.category = tk.Entry(self.win)
        self.category.pack()

        
        tk.Label(self.win, text="Amount").pack(pady=5)
        self.amount = tk.Entry(self.win)
        self.amount.pack()

        
        tk.Label(self.win, text="Notes").pack(pady=5)
        self.notes = tk.Entry(self.win)
        self.notes.pack()

        
        tk.Button(
            self.win,
            text="Save",
            bg="#6c63ff",
            fg="white",
            command=self.save_transaction
        ).pack(pady=15)

       
        if transaction:

            self.date.insert(0, transaction[1])
            self.category.insert(0, transaction[2])
            self.amount.insert(0, transaction[3])
            self.notes.insert(0, transaction[4])

   
    def save_transaction(self):

        date = self.date.get()
        category = self.category.get()
        amount = self.amount.get()
        notes = self.notes.get()

        conn = sqlite3.connect("data/expense_tracker.db")
        cur = conn.cursor()

        
        if self.transaction:

            cur.execute(
                """
                UPDATE transactions
                SET date=?, category=?, amount=?, notes=?
                WHERE id=?
                """,
                (date, category, amount, notes, self.transaction[0])
            )

     
        else:

            cur.execute(
                """
                INSERT INTO transactions(user_id,date,category,amount,notes)
                VALUES(?,?,?,?,?)
                """,
                (self.user_id, date, category, amount, notes)
            )

        conn.commit()
        conn.close()

        self.refresh_callback()
        self.win.destroy()