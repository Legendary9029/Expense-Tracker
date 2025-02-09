import sqlite3
import pandas as pd
from datetime import datetime

# Database connection
def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# Add expense to database
def add_expense(date, category, description, amount):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
        (date, category, description, amount),
    )
    conn.commit()
    conn.close()

# Fetch all expenses
def get_all_expenses():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return expenses

# Delete expense by ID
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# Update expense by ID
def update_expense(expense_id, date, category, description, amount):
    conn = get_db_connection()
    conn.execute(
        "UPDATE expenses SET date = ?, category = ?, description = ?, amount = ? WHERE id = ?",
        (date, category, description, amount, expense_id),
    )
    conn.commit()
    conn.close()