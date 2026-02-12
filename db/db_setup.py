
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "expense_tracker.db")

def get_conn():
    return sqlite3.connect(DB_PATH)

def setup_database():
    conn = get_conn()
    cur = conn.cursor()

    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT
    )
    """)

    
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
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database setup complete:", DB_PATH)

if __name__ == "__main__":

    setup_database()
