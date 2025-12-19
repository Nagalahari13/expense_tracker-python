import tkinter as tk
from tkinter import ttk
from gui.transaction_form import TransactionForm
from db.repository import get_all_transactions
from gui.category_window import CategoryWindow
from db.repository import get_all_budgets,get_total_spent_by_category
from gui.report_window import ReportWindow
from utils.import_export import (
    export_to_csv,
    import_from_csv,
    backup_database,
    restore_database
)


class MainWindow:
    def __init__(self, root, user_id, open_main_app):
        self.root = root
        self.user_id=user_id
        
        self.open_main_app=open_main_app
        self.root.title("Personal Expense Tracker")
        self.create_menu()
        self._create_main_content()
        self.load_transactions()
        
        
        title = tk.Label(
            self.root,
            text="Personal Expense Tracker",
            font=("Helvetica", 18, "bold")
        )
        title.pack(pady=10)


        # 🔹 Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Add Transaction",
            width=18
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="View Transactions",
            width=18
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            btn_frame,
            text="Logout",
            bg="#a9ff44",
            fg="white",
            width=18,
            command=self.logout
        ).grid(row=0, column=2, padx=10)
       
    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_command(label="Import from CSV", command=self.import_from_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Backup Database", command=self.backup_database)
        file_menu.add_command(label="Restore Database", command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="File", menu=file_menu)

    
        txn_menu = tk.Menu(menubar, tearoff=0)
        txn_menu.add_command(label="Add Transaction", command=self.open_transaction_form)
        txn_menu.add_command(label="Edit Transaction", command=self.edit_transaction)
        txn_menu.add_command(label="Delete Transaction", command=self.delete_transaction)
        txn_menu.add_command(label="Filter Transactions", command=self.open_filter_window)

        menubar.add_cascade(label="Transactions", menu=txn_menu)

    
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Dashboard", command=self.open_dashboard)
        report_menu.add_command(label="Reports", command=self.open_reports)
        report_menu.add_command(label="Budgets", command=self.open_budget_window)

        menubar.add_cascade(label="Reports", menu=report_menu)


        menubar.add_command(label="Categories", command=self.open_category_window)
        self.root.config(menu=menubar)

    def _create_main_content(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.budget_label = tk.Label(self.root,text="", font=("Arial",12),fg="blue")
        self.budget_label.pack(pady=5)

        columns = ("id","date", "type", "category", "amount", "payment_method", "tags", "notes")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("payment_method", text="Payment")
        self.tree.heading("tags", text="Tags")
        self.tree.heading("notes", text="Notes")
       


        for col in columns:
            self.tree.heading("id",text="")
            self.tree.column("id",width=0,stretch=False)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>",self.double_click_edit)

        # ========== ROOT LAYOUT ==========
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True)

        # ========== TOOLBAR ==========
        toolbar = ttk.Frame(main_container)
        toolbar.pack(fill="x", padx=10, pady=5)

        ttk.Button(toolbar, text="➕ Add", command=self.open_transaction_form).pack(side="left", padx=5)
        ttk.Button(toolbar, text="✏ Edit", command=self.edit_transaction).pack(side="left", padx=5)
        ttk.Button(toolbar, text="🗑 Delete", command=self.delete_transaction).pack(side="left", padx=5)
        ttk.Button(toolbar, text="🔍 Filter", command=self.open_filter_window).pack(side="left", padx=5)
        ttk.Button(toolbar, text="📊 Dashboard", command=self.open_dashboard).pack(side="left", padx=5)

        # ========== CONTENT AREA ==========
        content = ttk.Frame(main_container)
        content.pack(fill="both", expand=True)

        # ========== SIDEBAR ==========
        sidebar = ttk.Frame(content, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(sidebar, text="Navigation", font=("Arial", 11, "bold")).pack(pady=10)

        ttk.Button(sidebar, text="Manage Categories", command=self.open_category_window).pack(fill="x", pady=5)
        ttk.Button(sidebar, text="Manage Budgets", command=self.open_budget_window).pack(fill="x", pady=5)
        ttk.Button(sidebar, text="Reports", command=self.open_reports).pack(fill="x", pady=5)

        # ========== MAIN TABLE ==========
        table_frame = ttk.Frame(content)
        table_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.tree=ttk.Treeview(
            frame,
            columns = ( "id", "date", "type", "category", "amount", "payment_method", "tags", "notes"),
            show="headings"
        )
        columns=("id", "date", "type", "category", "amount", "payment_method", "tags", "notes")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120)
        
        self.tree.column("id", width=0, stretch=False)
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.double_click_edit)

        # ========== STATUS BAR ==========
        self.budget_label = tk.Label(
            self.root,
            text="",
            anchor="w",
            fg="blue"
        )
        self.budget_label.pack(fill="x", padx=10, pady=5)

        from utils.import_export import export_to_csv, import_from_csv, backup_database, restore_database

        ttk.Separator(self.root, orient="horizontal").pack(fill="x",pady=10)

        ttk.Button(self.root, text="Export to CSV", command=export_to_csv).pack(pady=3)
        ttk.Button(self.root, text="Import from CSV", command=import_from_csv).pack(pady=3)
        ttk.Button(self.root, text="Backup Database", command=backup_database).pack(pady=3)
        ttk.Button(self.root, text="Restore Database", command=restore_database).pack(pady=3)
            
    def refresh_category_dropdown(self):
        pass

    def open_transaction_form(self):
        TransactionForm(self, self.user_id)

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        from db.repository import get_all_transactions

        transactions = get_all_transactions(self.user_id)

        for t in transactions:
            self.tree.insert("", "end", values=t)
                
        self.refresh_budget_summary()

    def refresh_budget_summary(self):
        budgets = get_all_budgets()
        text = ""

        for b in budgets:
            budget_id, category, limit_amount = b

            spent = get_total_spent_by_category(category)

            if spent > limit_amount:
                text += f"{category}: ₹{spent} / ₹{limit_amount}  ❗ OVER BUDGET\n"
            else:
                text += f"{category}: ₹{spent} / ₹{limit_amount}\n"

        self.budget_label.config(text=text)  

    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = self.tree.item(item)["values"]
        TransactionForm(self, self.user_id, transaction=values)

    def double_click_edit(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = selected[0]
        values = self.tree.item(item)["values"]
        TransactionForm(self, self.user_id, transaction=values) 

    def update_transactions(self,rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in rows:
            self.tree.insert("","end",values=r)

    def open_filter_window(self):
        from gui.filter_window import FilterWindow
        FilterWindow(self) 

    def load_filtered_transactions(self,rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in rows:
            self.tree.insert("","end",values=(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
            )) 

    def open_dashboard(self):
        from gui.dashboard_window import DashboardWindow
        DashboardWindow(self.root, self.user_id)

    def open_budget_window(self):
        from gui.budget_window import BudgetWindow
        BudgetWindow(self, self.user_id)

    def open_reports(self):
        win = tk.Toplevel(self.root)
        ReportWindow(win, self)
    
    def open_category_window(self):
        CategoryWindow(self)

    def export_to_csv(self):
        export_to_csv()
    def import_from_csv(self):
        import_from_csv()
    def backup_database(self):
        backup_database()
    def restore_database(self):
        restore_database()

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            print("no row selected")
            return  # No row selected

        item = selected[0]
        values = self.tree.item(item)["values"]

        transaction_id = values[0]  # first column in DB row

        from db.repository import delete_transaction
        delete_transaction(transaction_id)

        self.load_transactions()
        self.tree.pack(fill="both", expand=True)
    def logout(self):
        self.root.destroy()   # close dashboard

        import tkinter as tk
        from gui.login_window import LoginWindow

        login_root = tk.Tk()
        LoginWindow(login_root, self.open_main_app)
        login_root.mainloop()
