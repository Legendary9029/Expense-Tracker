import sqlite3
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
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS recurring_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            end_date DATE,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            frequency TEXT NOT NULL  -- e.g., 'monthly', 'weekly'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            source TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS split_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            person_name TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (expense_id) REFERENCES expenses (id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            person_name TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            type TEXT NOT NULL  -- 'debt' or 'loan'
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

# Add recurring expense
def add_recurring_expense(start_date, end_date, category, description, amount, frequency):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO recurring_expenses (start_date, end_date, category, description, amount, frequency) VALUES (?, ?, ?, ?, ?, ?)",
        (start_date, end_date, category, description, amount, frequency),
    )
    conn.commit()
    conn.close()

# Fetch all recurring expenses
def get_recurring_expenses():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM recurring_expenses").fetchall()
    conn.close()
    return expenses

# Add income
def add_income(date, source, description, amount):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO income (date, source, description, amount) VALUES (?, ?, ?, ?)",
        (date, source, description, amount),
    )
    conn.commit()
    conn.close()

# Fetch all income
def get_all_income():
    conn = get_db_connection()
    income = conn.execute("SELECT * FROM income").fetchall()
    conn.close()
    return income

# Add split expense
def add_split_expense(expense_id, person_name, amount):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO split_expenses (expense_id, person_name, amount) VALUES (?, ?, ?)",
        (expense_id, person_name, amount),
    )
    conn.commit()
    conn.close()

# Fetch split expenses for a given expense ID
def get_split_expenses(expense_id):
    conn = get_db_connection()
    splits = conn.execute("SELECT * FROM split_expenses WHERE expense_id = ?", (expense_id,)).fetchall()
    conn.close()
    return splits

# Add debt/loan
def add_debt(date, person_name, description, amount, type):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO debts (date, person_name, description, amount, type) VALUES (?, ?, ?, ?, ?)",
        (date, person_name, description, amount, type),
    )
    conn.commit()
    conn.close()

# Fetch all debts/loans
def get_all_debts():
    conn = get_db_connection()
    debts = conn.execute("SELECT * FROM debts").fetchall()
    conn.close()
    return debts