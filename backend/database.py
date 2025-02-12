import email

from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, date
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Get MongoDB URI from .env
MONGODB_URI = os.getenv("MONGODB_URI")

# Validate URI
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in the environment variables.")

# Increase timeout to 60 seconds
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=60000)
db = client["expense_tracker"]

# Collections
users_collection = db["users"]
expenses_collection = db["expenses"]
income_collection = db["income"]

try:
    # Test connection
    client.server_info()
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

import re

def is_strong_password(password):
    """
    Check if the password is strong:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

def create_user(username, password, email):  # Add email as a parameter
    if users_collection.find_one({"username": username}):
        return False, "Username already exists."

    # Validate password strength
    is_valid, message = is_strong_password(password)
    if not is_valid:
        return False, message

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Ensure the email is stored in the database
    users_collection.insert_one({"username": username, "password": hashed_password, "email": email})

    return True, "Account created successfully!"


def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return True, "Authentication successful."
    return False, "Invalid username or password."

# Expense Operations
def add_expense(username, date_value, category, description, amount, currency="USD", recurring=False, recurrence_period=None):
    try:
        # Convert date to datetime object
        if isinstance(date_value, str):
            date_obj = datetime.strptime(date_value, "%Y-%m-%d")
        elif isinstance(date_value, date):  # Now we can properly check for date type
            date_obj = datetime.combine(date_value, datetime.min.time())
        elif isinstance(date_value, datetime):
            date_obj = date_value
        else:
            return False, f"Invalid date type: {type(date_value)}"

        expense = {
            "username": username,
            "date": date_obj,
            "category": category,
            "description": description,
            "amount": float(amount),
            "currency": currency,
            "recurring": recurring,
            "recurrence_period": recurrence_period if recurring and recurrence_period else None
        }
        expenses_collection.insert_one(expense)

        if recurring and recurrence_period and isinstance(recurrence_period, int):
            for i in range(1, 12):  # Auto-generate 12 future occurrences
                next_date = date_obj + timedelta(days=recurrence_period * i)
                expense_copy = expense.copy()
                expense_copy["date"] = next_date
                expenses_collection.insert_one(expense_copy)

        return True, "Expense added successfully."
    except ValueError as e:
        return False, f"Invalid date format: {str(e)}"
    except Exception as e:
        return False, f"Error adding expense: {str(e)}"

def get_expenses(username):
    expenses = list(expenses_collection.find({"username": username}, {"_id": 0}))
    return expenses if expenses else []

def delete_expense(expense_id):
    if not ObjectId.is_valid(expense_id):
        return False, "Invalid expense ID."
    result = expenses_collection.delete_one({"_id": ObjectId(expense_id)})
    return True, "Expense deleted." if result.deleted_count else False, "Expense not found."

def update_expense(expense_id, date, category, description, amount, currency="USD"):
    if not ObjectId.is_valid(expense_id):
        return False, "Invalid expense ID."

    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")  # Ensure correct date format
        elif isinstance(date, datetime.date):
            date = datetime.combine(date, datetime.min.time())  # Convert date to datetime
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

    update_data = {
        "date": date,
        "category": category,
        "description": description,
        "amount": float(amount),
        "currency": currency
    }

    result = expenses_collection.update_one(
        {"_id": ObjectId(expense_id)}, {"$set": update_data}
    )

    return True, "Expense updated." if result.modified_count else False, "Expense not found or no change made."

# Income Tracking
def add_income(username, date, source, amount, currency="USD"):
    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")  # Ensure correct date format
        elif isinstance(date, datetime.date):
            date = datetime.combine(date, datetime.min.time())  # Convert date to datetime
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

    income_collection.insert_one({
        "username": username,
        "date": date,
        "source": source,
        "amount": float(amount),
        "currency": currency
    })
    return True, "Income added successfully."

def get_income(username):
    income = list(income_collection.find({"username": username}, {"_id": 0}))
    return income if income else []

def delete_income(income_id):
    if not ObjectId.is_valid(income_id):
        return False, "Invalid income ID."
    result = income_collection.delete_one({"_id": ObjectId(income_id)})
    return True, "Income deleted." if result.deleted_count else False, "Income not found."

def update_income(income_id, date, source, amount, currency="USD"):
    if not ObjectId.is_valid(income_id):
        return False, "Invalid income ID."

    try:
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")  # Ensure correct date format
        elif isinstance(date, datetime.date):
            date = datetime.combine(date, datetime.min.time())  # Convert date to datetime
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

    update_data = {
        "date": date,
        "source": source,
        "amount": float(amount),
        "currency": currency
    }

    result = income_collection.update_one(
        {"_id": ObjectId(income_id)}, {"$set": update_data}
    )

    return True, "Income updated." if result.modified_count else False, "Income not found or no change made."

# Add these collections
recurring_expenses_collection = db["recurring_expenses"]
split_expenses_collection = db["split_expenses"]
debts_collection = db["debts"]

# Recurring Expenses
def add_recurring_expense(username, start_date, end_date, category, description, amount, frequency):
    recurring_expense = {
        "username": username,
        "start_date": start_date,
        "end_date": end_date,
        "category": category,
        "description": description,
        "amount": float(amount),
        "frequency": frequency
    }
    recurring_expenses_collection.insert_one(recurring_expense)
    return True, "Recurring expense added successfully."

def get_recurring_expenses(username):
    expenses = list(recurring_expenses_collection.find({"username": username}, {"_id": 0}))
    return expenses if expenses else []

# Expense Splitting
def add_split_expense(username, expense_id, person_name, amount):
    split_expense = {
        "username": username,
        "expense_id": expense_id,
        "person_name": person_name,
        "amount": float(amount)
    }
    split_expenses_collection.insert_one(split_expense)
    return True, "Expense split successfully."

def get_split_expenses(username, expense_id):
    splits = list(split_expenses_collection.find({"username": username, "expense_id": expense_id}, {"_id": 0}))
    return splits if splits else []

# Debt & Loan Tracking
def add_debt(username, date, person_name, description, amount, type):
    debt = {
        "username": username,
        "date": date,
        "person_name": person_name,
        "description": description,
        "amount": float(amount),
        "type": type
    }
    debts_collection.insert_one(debt)
    return True, "Debt/Loan added successfully."

def get_debts(username):
    debts = list(debts_collection.find({"username": username}, {"_id": 0}))
    return debts if debts else []