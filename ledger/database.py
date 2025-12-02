import sqlite3

DB_FILE = 'db.sqlite3'

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (transaction_id TEXT PRIMARY KEY, amount REAL, date TEXT, name TEXT, category TEXT)''')
    conn.commit()
    conn.close()

def save_transaction(txn_data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO transactions (transaction_id, amount, date, name, category)
                 VALUES (?, ?, ?, ?, ?)''', 
                 (txn_data['transaction_id'], txn_data['amount'], txn_data['date'], txn_data['name'], str(txn_data['category'])))
    conn.commit()
    conn.close()

def get_monthly_summary(month):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM transactions")
    result = c.fetchone()
    conn.close()
    return {"total": result[0] if result[0] else 0.0}
