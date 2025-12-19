import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import sqlite3
from gui.report_window import ReportWindow
import ttkbootstrap as tb
from ttkbootstrap.constants import *

from tkinter import messagebox



class DashboardWindow(tb.Frame):
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id=user_id

        # 🔹 CREATE REAL WINDOW
        self.win = tk.Toplevel(parent.root)
        self.win.title("Dashboard")
        self.win.geometry("900x600")

        # 🔹 ATTACH FRAME TO WINDOW
        super().__init__(self.win)
        self.pack(fill="both", expand=True)


        
        title = tk.Label(
            self,
            text="Personal Expense Dashboard",
            font=("Helvetica", 20, "bold"),
            bg="#f5f5f5",
            fg="#333"
        )
        title.pack(pady=15)
        
        logout_btn = tk.Button(
            self.win,
            text="Logout",
            bg="#ff4d4d",
            fg="white",
            command=self.destroy
        )
        logout_btn.pack(anchor="ne", padx=10, pady=10)

     
        filter_frame = tk.Frame(self, bg="#f5f5f5")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Year:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, padx=5)
        self.year_var = tk.IntVar(value=datetime.now().year)
        tk.Entry(filter_frame, textvariable=self.year_var, width=10).grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Month:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=2, padx=5)
        self.month_var = tk.IntVar(value=datetime.now().month)
        tk.Entry(filter_frame, textvariable=self.month_var, width=10).grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Refresh Dashboard",
                   command=self.load_dashboard).grid(row=0, column=4, padx=10)

        # -------------------- GRAPH FRAME --------------------
        self.graph_frame = tk.Frame(self, bg="#11cf33")
        self.graph_frame.pack(fill="both", expand=True, pady=10)

        self.load_dashboard()

    # ---------------------------------------------------------
    #   LOAD GRAPHS
    # ---------------------------------------------------------
    def load_dashboard(self):
        
        data=repr.get_dashboard_data(self.user_id)
        print("Dashboard data", data)
        try:
        # Clear old graphs
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            year = self.year_var.get()
            month = self.month_var.get()

            category_data = self.get_category_summary(year, month)
            month_data = self.get_monthly_summary(year)

        # ---------------- LEFT GRAPH ----------------
            left_frame = tk.Frame(self.graph_frame, bg="#f5f5f5")
            left_frame.pack(side="left", fill="both", expand=True)

            if category_data:
                categories = [c[0] for c in category_data]
                amounts = [c[1] for c in category_data]

                fig1 = plt.Figure(figsize=(4.5, 4.5), dpi=100)
                ax1 = fig1.add_subplot(111)
                ax1.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
                ax1.set_title("Category-wise Spending")

                canvas1 = FigureCanvasTkAgg(fig1, master=left_frame)
                canvas1.draw()
                canvas1.get_tk_widget().pack(fill="both", expand=True)
            else:
                tk.Label(
                    left_frame,
                    text="Dashboard loaded",
                    font=("Arial", 14, "bold"),
                    fg="green"
                ).pack(pady=10)
            print("category data", category_data)
            print("month data", month_data)

        # ---------------- RIGHT GRAPH ----------------
            right_frame = tk.Frame(self.graph_frame, bg="#f5f5f5")
            right_frame.pack(side="right", fill="both", expand=True)

            if month_data:
                months = [int(m[0]) for m in month_data]
                income = [m[1] for m in month_data]
                expense = [m[2] for m in month_data]

                fig2 = plt.Figure(figsize=(5, 4.5), dpi=100)
                ax2 = fig2.add_subplot(111)
                ax2.plot(months, income, marker="o", label="Income")
                ax2.plot(months, expense, marker="o", label="Expense")
                ax2.set_title("Monthly Income vs Expense")
                ax2.legend()

                canvas2 = FigureCanvasTkAgg(fig2, master=right_frame)
                canvas2.draw()
                canvas2.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            print("DASHBOARD ERROR:", e)
        
    # ---------------------------------------------------------
    def get_category_summary(self, year, month):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT category, SUM(amount)
            FROM transactions
            WHERE user_id=?
                AND type='expense'
                AND substr(date, 7, 4)= ?
                AND substr(date, 4, 2) = ?
            GROUP BY category
        """, (
            self.parent.user_id,
            str(year),
            f"{int(month):02d}"
        ))
        
        data = cur.fetchall()
        conn.close()
        return data

    def get_monthly_summary(self, year):
        conn = sqlite3.connect("expense_tracker.db")
        cur = conn.cursor()

        cur.execute("""
            SELECT substr(date, 4, 2) AS month,
                   SUM(CASE WHEN type='income' THEN amount ELSE 0 END),
                   SUM(CASE WHEN type='expense' THEN amount ELSE 0 END)
            FROM transactions
            WHERE user_id=?
                AND substr(date, 7, 4)= ?
            GROUP BY month
            ORDER BY month
        """, (
            self.parent.user_id,
            str(year)
        ))

        data = cur.fetchall()
        conn.close()
        return data
    
