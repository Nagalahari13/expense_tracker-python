import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from db.repository import get_filtered_transactions, get_all_categories

class FilterWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.title("Filter Transactions")
        self.geometry("400x450")

        # ---- DATE RANGE ----
        ttk.Label(self, text="From Date:").pack(anchor="w", padx=10, pady=5)
        self.from_date = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.from_date.pack(fill="x", padx=10)

        ttk.Label(self, text="To Date:").pack(anchor="w", padx=10, pady=5)
        self.to_date = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.to_date.pack(fill="x", padx=10)

        # ---- TYPE ----
        ttk.Label(self, text="Type:").pack(anchor="w", padx=10, pady=5)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(
            self, textvariable=self.type_var, values=["", "income", "expense"]
        )
        self.type_dropdown.pack(fill="x", padx=10)

        # ---- CATEGORY ----
        ttk.Label(self, text="Category:").pack(anchor="w", padx=10, pady=5)
        self.category_var = tk.StringVar()
        categories = [""] + get_all_categories()
        self.category_dropdown = ttk.Combobox(
            self, textvariable=self.category_var, values=categories
        )
        self.category_dropdown.pack(fill="x", padx=10)

        # ---- AMOUNT RANGE ----
        ttk.Label(self, text="Min Amount:").pack(anchor="w", padx=10, pady=5)
        self.min_amount = tk.Entry(self)
        self.min_amount.pack(fill="x", padx=10)

        ttk.Label(self, text="Max Amount:").pack(anchor="w", padx=10, pady=5)
        self.max_amount = tk.Entry(self)
        self.max_amount.pack(fill="x", padx=10)

        # ---- TAGS ----
        ttk.Label(self, text="Tags:").pack(anchor="w", padx=10, pady=5)
        self.tags_entry = tk.Entry(self)
        self.tags_entry.pack(fill="x", padx=10)

        # ---- BUTTONS ----
        ttk.Button(self, text="Apply Filter", command=self.apply_filter).pack(pady=10)
        ttk.Button(self, text="Clear Filter", command=self.clear_filter).pack(pady=5)

    # ----------------------------------------------------------
    def apply_filter(self):
        filters = {
            "from_date": self.from_date.get(),
            "to_date": self.to_date.get(),
            "type": self.type_var.get(),
            "category": self.category_var.get(),
            "min_amount": self.min_amount.get(),
            "max_amount": self.max_amount.get(),
            "tags": self.tags_entry.get()
        }

        results = get_filtered_transactions(filters)
        self.main_window.update_transactions(results)

    # ----------------------------------------------------------
    def clear_filter(self):
        self.main_window.load_transactions()
        self.destroy()