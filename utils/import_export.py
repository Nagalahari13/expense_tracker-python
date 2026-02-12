import csv
import shutil
import os
import sqlite3
from tkinter import filedialog, messagebox

DB_PATH = "expense.db"


def export_to_csv():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    headers = [description[0] for description in cur.description]
    conn.close()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    messagebox.showinfo("Success", "Transactions exported successfully!")



def import_from_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)  # skip header

        for row in reader:
            cur.execute("""
                INSERT INTO transactions
                (id, date, type, category, amount, payment_method, tags, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, row)

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Transactions imported successfully!")



def backup_database():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".db",
        filetypes=[("Database files", "*.db")]
    )

    if not file_path:
        return

    shutil.copy(DB_PATH, file_path)
    messagebox.showinfo("Backup", "Database backup completed!")



def restore_database():
    file_path = filedialog.askopenfilename(
        filetypes=[("Database files", "*.db")]
    )

    if not file_path:
        return

    shutil.copy(file_path, DB_PATH)

    messagebox.showinfo("Restore", "Database restored! Restart the app.")
