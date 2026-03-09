import sqlite3
from pathlib import Path

DB_FILE = Path("expense_tracker.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT,
                tags TEXT,
                notes TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            
                );
            """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
            """)

    conn.commit()
    conn.close()
def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)

    conn.commit()
    conn.close()


