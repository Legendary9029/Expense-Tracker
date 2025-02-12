import streamlit as st
from backend.database import create_user, authenticate_user, add_expense, get_expenses, delete_expense, update_expense
from backend.expenses import calculate_monthly_spending, calculate_category_spending, calculate_daily_spending, get_expenses_df
from backend.utils import validate_expense, check_budget, send_email_notification
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Initialize session state for user authentication
if "username" not in st.session_state:
    st.session_state.username = None

# Login/Signup Page
def login_signup_page():
    st.title("💰 Expense Tracker")
    st.header("Login / Signup")
    choice = st.radio("Choose an option", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            success, message = authenticate_user(username, password)
            if success:
                st.session_state.username = username
                st.success(message)
                st.experimental_rerun()
            else:
                st.error(message)
    else:
        if st.button("Signup"):
            success, message = create_user(username, password)
            if success:
                st.success(message)
            else:
                st.error(message)

# Main App Page
def main_app_page():
    st.title("💰 Expense Tracker")
    st.header(f"Welcome, {st.session_state.username}!")

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
                add_expense(st.session_state.username, date, category, description, amount)
                st.success("Expense added successfully!")
            else:
                st.error(message)

    # Main content area
    st.header("Your Expenses")
    expenses_df = get_expenses_df(st.session_state.username)

    if not expenses_df.empty:
        st.dataframe(expenses_df, use_container_width=True)

        # Visualizations
        st.header("📊 Visualizations")

        # Daily Spending
        st.subheader("Daily Spending")
        daily_spending = calculate_daily_spending(expenses_df)
        fig, ax = plt.subplots()
        sns.lineplot(x="date", y="amount", data=daily_spending, ax=ax)
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Amount")
        st.pyplot(fig)

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

        # Budget Tracking
        st.header("💸 Budget Tracking")
        budget = st.number_input("Set Your Monthly Budget", min_value=0.0, format="%.2f")
        user_email = st.text_input("Enter your email for notifications")
        if budget > 0 and user_email:
            total_spent = monthly_spending["amount"].sum()
            st.write(f"Total Spent This Month: ${total_spent:.2f}")
            st.write(f"Remaining Budget: ${budget - total_spent:.2f}")
            alert_message = check_budget(total_spent, budget)
            if "exceeded" in alert_message:
                st.error(alert_message)
                if send_email_notification(
                    "Budget Exceeded",
                    f"You have exceeded your monthly budget. Total spent: ${total_spent:.2f}",
                    user_email,
                ):
                    st.success("Notification sent to your email!")
            else:
                st.success(alert_message)
    else:
        st.info("No expenses added yet. Start by adding an expense in the sidebar!")

# Run the app
if st.session_state.username:
    main_app_page()
else:
    login_signup_page()