import streamlit as st
from PIL.Image import Image
from backend.database import (
    create_user, authenticate_user, add_expense, get_expenses, delete_expense, update_expense,
    add_income, add_recurring_expense, add_split_expense, add_debt
)
from backend.expenses import (
    calculate_monthly_spending, calculate_category_spending, calculate_daily_spending, get_expenses_df
)
from backend.utils import (
    validate_expense, check_budget, send_email_notification, extract_text_from_image,
    train_expense_categorizer, predict_category
)
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
    elif choice == "Signup":
        email = st.text_input("Email")  # Add email input
        if st.button("Signup"):
            success, message = create_user(username, password, email)
            if success:
                st.success(message)
            else:
                st.error(message)

# Main App Page
def main_app_page():
    st.title("💰 Expense Tracker")
    st.header(f"Welcome, {st.session_state.username}!")

    # Sidebar for adding expenses, recurring expenses, income, etc.
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

        # Recurring Expenses
        st.header("Add Recurring Expense")
        start_date = st.date_input("Start Date", datetime.today())
        end_date = st.date_input("End Date (optional)", None)
        recurring_category = st.selectbox("Recurring Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
        recurring_description = st.text_input("Recurring Description")
        recurring_amount = st.number_input("Recurring Amount", min_value=0.0, format="%.2f")
        frequency = st.selectbox("Frequency", ["Monthly", "Weekly"])
        if st.button("Add Recurring Expense"):
            add_recurring_expense(st.session_state.username, start_date, end_date, recurring_category, recurring_description, recurring_amount, frequency)
            st.success("Recurring expense added successfully!")

        # Income Tracking
        st.header("Add Income")
        income_date = st.date_input("Income Date", datetime.today())
        source = st.text_input("Income Source")
        income_description = st.text_input("Income Description")
        income_amount = st.number_input("Income Amount", min_value=0.0, format="%.2f")
        if st.button("Add Income"):
            add_income(st.session_state.username, income_date, source, income_description, income_amount)
            st.success("Income added successfully!")

        # Expense Splitting
        # Fetch the user's expenses before using it anywhere
        expenses_df = get_expenses_df(st.session_state.username)

        # Ensure the DataFrame is not empty before accessing its values
        if expenses_df.empty:
            st.warning("No expenses available to split. Please add an expense first.")
        else:
            # Expense Splitting
            st.header("Split Expense")
            expense_to_split = st.selectbox("Select Expense to Split", expenses_df["description"])
            split_amount = st.number_input("Total Amount to Split", min_value=0.0, format="%.2f")
            num_people = st.number_input("Number of People", min_value=1, step=1)

            # Collect names dynamically
            person_names = []
            for i in range(num_people):
                person_name = st.text_input(f"Person {i + 1} Name")
                if person_name:
                    person_names.append(person_name)

            if st.button("Split Expense"):
                if not person_names or len(person_names) != num_people:
                    st.error("Please enter names for all people.")
                else:
                    per_person_amount = split_amount / num_people
                    expense_id = expenses_df[expenses_df["description"] == expense_to_split].iloc[0]["id"]
                    for person in person_names:
                        add_split_expense(st.session_state.username, expense_id, person, per_person_amount)
                    st.success("Expense split successfully!")

        # Debt & Loan Tracking
        st.header("Add Debt/Loan")
        debt_date = st.date_input("Debt/Loan Date", datetime.today())
        person_name = st.text_input("Person Name")
        debt_description = st.text_input("Debt/Loan Description")
        debt_amount = st.number_input("Debt/Loan Amount", min_value=0.0, format="%.2f")
        debt_type = st.selectbox("Type", ["Debt", "Loan"])
        if st.button("Add Debt/Loan"):
            add_debt(st.session_state.username, debt_date, person_name, debt_description, debt_amount, debt_type)
            st.success("Debt/Loan added successfully!")

    # Main content area
    st.header("Your Expenses")
    expenses_df = get_expenses_df(st.session_state.username)

    if not expenses_df.empty:
        st.dataframe(expenses_df, use_container_width=True)

        # Visualizations
        # Apply Seaborn's dark theme for a modern look
        sns.set_style("darkgrid")
        sns.set_palette("pastel")

        st.header("📊 Visualizations")

        # 📈 **Daily Spending**
        st.subheader("Daily Spending")
        daily_spending = calculate_daily_spending(expenses_df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(x="date", y="amount", data=daily_spending, marker="o", markersize=8, linewidth=2, ax=ax)
        ax.set_xlabel("Date", fontsize=12, fontweight="bold")
        ax.set_ylabel("Total Amount ($)", fontsize=12, fontweight="bold")
        ax.set_title("Daily Spending Trend", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # 📊 **Monthly Spending**
        st.subheader("Monthly Spending")
        monthly_spending = calculate_monthly_spending(expenses_df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="month", y="amount", data=monthly_spending, ax=ax, edgecolor="black", linewidth=2)
        ax.set_xlabel("Month", fontsize=12, fontweight="bold")
        ax.set_ylabel("Total Amount ($)", fontsize=12, fontweight="bold")
        ax.set_title("Monthly Spending Breakdown", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # 🥧 **Category-wise Breakdown**
        st.subheader("Category-wise Breakdown")
        category_spending = calculate_category_spending(expenses_df)
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = sns.color_palette("pastel")
        ax.pie(category_spending["amount"], labels=category_spending["category"], autopct="%1.1f%%", colors=colors,
               startangle=140)
        ax.set_title("Spending by Category", fontsize=14, fontweight="bold")
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

        # OCR-Based Receipt Upload
        st.header("📄 Upload Receipt")
        uploaded_file = st.file_uploader("Upload Receipt", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            extracted_text = extract_text_from_image(image)
            st.write("Extracted Text:", extracted_text)

        # AI-Powered Categorization
        st.header("🤖 AI-Powered Categorization")
        model, vectorizer = train_expense_categorizer(expenses_df)
        description = st.text_input("Enter Expense Description")
        if description:
            predicted_category = predict_category(model, vectorizer, description)
            st.write(f"Predicted Category: {predicted_category}")

    else:
        st.info("No expenses added yet. Start by adding an expense in the sidebar!")

# Run the app
if st.session_state.username:
    main_app_page()
else:
    login_signup_page()