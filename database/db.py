import sqlite3
import os

DB_PATH = os.path.join("data", "expense_tracker.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        category TEXT,
        amount REAL,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()