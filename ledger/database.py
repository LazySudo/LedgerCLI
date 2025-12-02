import sqlite3
import os
from typing import Dict, Any

DB_FILE = 'db.sqlite3'

def get_connection():
    """Create a connection to the local SQLite database."""
    return sqlite3.connect(DB_FILE)

def init_db():
    """Initialize the database schema if it does not exist."""
    conn = get_connection()
    c = conn.cursor()
    
    # Create Transactions Table
    # Added 'category' field to store AI-generated tags
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_id TEXT,
            amount REAL,
            date TEXT,
            name TEXT,
            category TEXT
        )
    ''')
    
    # Create Accounts Table (Optional structure for future use)
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            name TEXT,
            official_name TEXT,
            type TEXT,
            subtype TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_transaction(txn_data: Dict[str, Any]):
    """
    Save a single transaction to the database.
    Uses INSERT OR REPLACE to handle duplicate syncs gracefully.
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Handle list-based categories from Plaid by converting to string
    category_str = str(txn_data.get('category', 'Uncategorized'))
    
    c.execute('''
        INSERT OR REPLACE INTO transactions (transaction_id, account_id, amount, date, name, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        txn_data['transaction_id'],
        txn_data['account_id'],
        txn_data['amount'],
        txn_data['date'],
        txn_data['name'],
        category_str
    ))
    
    conn.commit()
    conn.close()

def get_monthly_summary(month: str = 'current') -> Dict[str, float]:
    """
    Calculate total spending for a given month.
    
    Args:
        month (str): Currently accepts 'current' or YYYY-MM format.
                    (Note: Real implementation would filter SQL by date string)
    
    Returns:
        dict: {'total': float, 'count': int}
    """
    conn = get_connection()
    c = conn.cursor()
    
    # In a full implementation, you would use: 
    # WHERE strftime('%Y-%m', date) = ?
    
    c.execute("SELECT SUM(amount), COUNT(*) FROM transactions")
    result = c.fetchone()
    
    conn.close()
    
    total = result[0] if result[0] else 0.0
    count = result[1] if result[1] else 0
    
    return {"total": total, "count": count}