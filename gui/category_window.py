import tkinter as tk
from tkinter import ttk
from db.repository import insert_category, get_all_categories


class CategoryWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.root)  
        self.parent = parent            
        self.title("Manage Categories")
        self.geometry("350x350")

        
        ttk.Label(self, text="New Category:").pack(pady=10)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(fill="x", padx=20)

        ttk.Button(
            self,
            text="Add Category",
            command=self.add_category
        ).pack(pady=10)

        
        ttk.Label(self, text="Existing Categories:").pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=20)

       
        self.load_categories()

   
    def add_category(self):
        name = self.name_entry.get().strip()

        if not name:
            return
        
        from db.repository import insert_category
        insert_category(name)       
        self.load_categories()      
        self.name_entry.delete(0, tk.END)

            
        if hasattr(self.parent,"refresh_category_dropdown"):
            self.parent.refresh_category_dropdown()

    def load_categories(self):
        self.listbox.delete(0, tk.END)

        for c in get_all_categories():     
            self.listbox.insert(tk.END, c)
    def refresh_categories(self):
        self.category_listbox.delete(0, tk.END)
        for cat in get_all_categories():
            self.category_listbox.insert(tk.END, cat) 