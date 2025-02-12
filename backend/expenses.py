import pandas as pd
from backend.database import get_expenses


# Get expenses as a DataFrame
def get_expenses_df(username):
    expenses = get_expenses(username)
    print("Raw expenses data:", expenses)  # Debug print

    if not expenses:  # Handle empty expense list
        return pd.DataFrame(columns=['date', 'category', 'description', 'amount', 'currency'])

    df = pd.DataFrame(expenses)
    print("DataFrame columns:", df.columns)  # Debug print

    if 'date' in df.columns:  # Safely convert date
        df['date'] = pd.to_datetime(df['date'])
    else:
        print("Warning: 'date' column not found in DataFrame")

    return df


# Filter expenses by date range, category, and amount
def filter_expenses(df, date_range=None, category=None, amount_range=None):
    if date_range:
        df = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]
    if category and category != "All":
        df = df[df["category"] == category]
    if amount_range:
        df = df[(df["amount"] >= amount_range[0]) & (df["amount"] <= amount_range[1])]
    return df


# Calculate daily spending
def calculate_daily_spending(df):
    return df.groupby(df["date"].dt.date)["amount"].sum().reset_index()


# Calculate monthly spending
def calculate_monthly_spending(df):
    df["month"] = df["date"].dt.to_period("M")
    return df.groupby("month")["amount"].sum().reset_index()


# Calculate category-wise spending
def calculate_category_spending(df):
    return df.groupby("category")["amount"].sum().reset_index()
