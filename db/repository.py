
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "expense_tracker.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


def insert_transaction(user_id, date, type, category, amount, payment_method, tags, notes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (user_id, date, type, category, amount, payment_method, tags, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, type, category, amount, payment_method, tags, notes))
    conn.commit()
    conn.close()

def get_all_transactions(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id
            date,
            type,
            category,
            amount,
            payment_method,
            tags,
            notes
        FROM transactions
        WHERE user_id=?
        ORDER BY date DESC
    """,(user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def update_transaction(transaction_id, date, type_, category, amount, payment_method, tags, notes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE transactions
        SET date = ?, type = ?, category = ?, amount = ?, payment_method = ?, tags = ?, notes = ?
        WHERE id = ?
    """, (date, type, category, amount, payment_method, tags, notes, transaction_id))
    conn.commit()
    conn.close()

def delete_transaction(transaction_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()


def insert_category(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories (name) VALUES (?)", (name, ))
    conn.commit()
    conn.close()

def get_all_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM categories ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows]

def delete_category(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE name = ?", (name,))
    conn.commit()
    conn.close()


def get_total_spent_by_category(category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE category = ? AND type = 'expense'
    """, (category,))
    result = cur.fetchone()
    conn.close()
    return result[0]

def get_all_budgets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, category, amount FROM budgets")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_budget(category, amount, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO budgets(category, amount, user_id) VALUES (?, ?, ?)", (category, amount, user_id))
    conn.commit()
    conn.close()

def delete_budget(budget_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
    conn.commit()
    conn.close()

def update_budget(budget_id, category, amount):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE budgets SET category = ?, amount = ? WHERE id = ?", (category, amount, budget_id))
    conn.commit()
    conn.close()
def get_category_summary(user_id, year, month):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id=?
        AND strftime('%Y', date) = ?
        AND strftime('%m', date) = ?
        GROUP BY category
    """, (user_id, str(year), f"{month:02d}"))

    data = cur.fetchall()
    conn.close()
    return data


def get_monthly_summary(user_id, year):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT strftime('%m', date) AS month,
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END),
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END)
        FROM transactions
        WHERE user_id=?
        AND strftime('%Y', date) = ?
        GROUP BY month
        ORDER BY month
    """, (user_id, str(year)))

    data = cur.fetchall()
    conn.close()
    return data
def get_category_summary(user_id, year, month):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id=?
          AND type='expense'
          AND strftime('%Y', date) = ?
          AND strftime('%m', date) = ?
        GROUP BY category
    """, (user_id, str(year), f"{month:02d}"))
    
    data = cur.fetchall()
    conn.close()
    return data


def get_monthly_summary(user_id, year):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT strftime('%m', date) AS month,
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_expense
        FROM transactions
        WHERE user_id=?
            AND strftime('%Y', date) = ?
        GROUP BY month
        ORDER BY month
    """, (user_id, str(year),))

    data = cur.fetchall()
    conn.close()
    return data
def get_filtered_transactions( start_date=None, end_date=None, category=None, tx_type=None):
    conn = sqlite3.connect("expense_tracker.db")
    cur = conn.cursor()

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    if category:
        query += " AND category = ?"
        params.append(category)

    if tx_type:
        query += " AND type = ?"
        params.append(tx_type)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows
def register_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()
    return user
def get_dashboard_data(self, user_id):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()

    return data
