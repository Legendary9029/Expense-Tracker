import pandas as pd
from backend.database import get_all_expenses

# Get expenses as a DataFrame
def get_expenses_df():
    expenses = get_all_expenses()
    return pd.DataFrame(expenses, columns=["id", "date", "category", "description", "amount"])

# Filter expenses by date range, category, and amount
def filter_expenses(df, date_range=None, category=None, amount_range=None):
    if date_range:
        df = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]
    if category and category != "All":
        df = df[df["category"] == category]
    if amount_range:
        df = df[(df["amount"] >= amount_range[0]) & (df["amount"] <= amount_range[1])]
    return df

# Calculate monthly spending
def calculate_monthly_spending(df):
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    return df.groupby("month")["amount"].sum().reset_index()

# Calculate category-wise spending
def calculate_category_spending(df):
    return df.groupby("category")["amount"].sum().reset_index()