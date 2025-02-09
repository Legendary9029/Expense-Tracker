import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from backend.database import init_db, add_expense, delete_expense, update_expense
from backend.expenses import get_expenses_df, filter_expenses, calculate_monthly_spending, calculate_category_spending
from backend.utils import validate_expense

# Initialize database
init_db()

# Set page title and layout
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker")

# Sidebar for adding expenses
with st.sidebar:
    st.header("Add New Expense")
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Expense"):
        is_valid, message = validate_expense(date, category, description, amount)
        if is_valid:
            add_expense(date, category, description, amount)
            st.success("Expense added successfully!")
        else:
            st.error(message)

# Main content area
st.header("Your Expenses")
expenses_df = get_expenses_df()

if not expenses_df.empty:
    st.dataframe(expenses_df, use_container_width=True)

    # Visualizations
    st.header("📊 Visualizations")

    # Monthly Spending
    st.subheader("Monthly Spending")
    monthly_spending = calculate_monthly_spending(expenses_df)
    fig, ax = plt.subplots()
    sns.barplot(x="month", y="amount", data=monthly_spending, ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount")
    st.pyplot(fig)

    # Category-wise Breakdown
    st.subheader("Category-wise Breakdown")
    category_spending = calculate_category_spending(expenses_df)
    fig, ax = plt.subplots()
    sns.barplot(x="category", y="amount", data=category_spending, ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Amount")
    st.pyplot(fig)

    # Filter Expenses
    st.header("🔍 Filter Expenses")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_date_range = st.date_input("Filter by Date Range", [])
    with col2:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(expenses_df["category"].unique()))
    with col3:
        filter_amount = st.slider("Filter by Amount", float(expenses_df["amount"].min()), float(expenses_df["amount"].max()), (0.0, float(expenses_df["amount"].max())))

    filtered_expenses = filter_expenses(expenses_df, filter_date_range, filter_category, filter_amount)
    st.dataframe(filtered_expenses, use_container_width=True)

    # Export Data
    st.header("📤 Export Data")
    if st.button("Export to CSV"):
        csv = expenses_df.to_csv(index=False).encode("utf-8")
        st.download_button(label="Download CSV", data=csv, file_name="expenses.csv", mime="text/csv")

    # Budget Tracking
    st.header("💸 Budget Tracking")
    budget = st.number_input("Set Your Monthly Budget", min_value=0.0, format="%.2f")
    if budget > 0:
        total_spent = monthly_spending["amount"].sum()
        st.write(f"Total Spent This Month: ${total_spent:.2f}")
        st.write(f"Remaining Budget: ${budget - total_spent:.2f}")
        if total_spent > budget:
            st.error("You have exceeded your budget!")
        else:
            st.success("You are within your budget.")

    # Edit/Delete Expenses
    st.header("✏️ Edit/Delete Expenses")
    edit_index = st.number_input("Enter the index of the expense to edit/delete", min_value=0, max_value=len(expenses_df) - 1, value=0)
    if st.button("Edit Expense"):
        update_expense(expenses_df.iloc[edit_index]["id"], date, category, description, amount)
        st.success("Expense updated successfully!")
    if st.button("Delete Expense"):
        delete_expense(expenses_df.iloc[edit_index]["id"])
        st.success("Expense deleted successfully!")
else:
    st.info("No expenses added yet. Start by adding an expense in the sidebar!")