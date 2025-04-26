import sqlite3

conn = sqlite3.connect('budgetbuddy.db')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    date TEXT,
    amount REAL,
    category TEXT,
    type TEXT
)""")
conn.commit()

def add_transaction(user, date, amount, category, type_):
    cursor.execute("INSERT INTO transactions (user, date, amount, category, type) VALUES (?, ?, ?, ?, ?)",
                   (user, date, amount, category, type_))
    conn.commit()

def get_transactions(user):
    cursor.execute("SELECT * FROM transactions WHERE user = ?", (user,))
    return cursor.fetchall()
