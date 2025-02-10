import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from PIL import Image
from backend.database import (
    init_db,
    add_expense,
    delete_expense,
    update_expense,
    add_recurring_expense,
    get_recurring_expenses,
    add_income,
    get_all_income,
    get_all_expenses,
    add_split_expense,
    get_split_expenses,
    add_debt,
    get_all_debts,
)
from backend.expenses import (
    get_expenses_df,
    filter_expenses,
    calculate_monthly_spending,
    calculate_category_spending,
)
from backend.utils import (
    validate_expense,
    check_budget,
    convert_currency,
    train_expense_categorizer,
    predict_category,
    extract_text_from_image,
    send_email_notification,
)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Initialize database
init_db()

# Set page title and layout
st.set_page_config(page_title="Expense Tracker", layout="wide")
st.title("💰 Expense Tracker")

# Dark Mode Toggle
st.sidebar.header("Settings")
dark_mode = st.sidebar.checkbox("Dark Mode")
if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar for adding expenses, recurring expenses, and income
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

    st.header("Add Recurring Expense")
    start_date = st.date_input("Start Date", datetime.today())
    end_date = st.date_input("End Date (optional)", None)
    recurring_category = st.selectbox("Recurring Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    recurring_description = st.text_input("Recurring Description")
    recurring_amount = st.number_input("Recurring Amount", min_value=0.0, format="%.2f")
    frequency = st.selectbox("Frequency", ["Monthly", "Weekly"])
    if st.button("Add Recurring Expense"):
        add_recurring_expense(start_date, end_date, recurring_category, recurring_description, recurring_amount, frequency)
        st.success("Recurring expense added successfully!")

    st.header("Add Income")
    income_date = st.date_input("Income Date", datetime.today())
    source = st.text_input("Income Source")
    income_description = st.text_input("Income Description")
    income_amount = st.number_input("Income Amount", min_value=0.0, format="%.2f")
    if st.button("Add Income"):
        add_income(income_date, source, income_description, income_amount)
        st.success("Income added successfully!")

# Main content area
st.header("Your Expenses")
expenses_df = get_expenses_df()
income_df = pd.DataFrame(get_all_income(), columns=["id", "date", "source", "description", "amount"])

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
    user_email = st.text_input("Enter your email for notifications")  # Add email input
    if budget > 0 and user_email:
        total_spent = monthly_spending["amount"].sum()
        st.write(f"Total Spent This Month: ${total_spent:.2f}")
        st.write(f"Remaining Budget: ${budget - total_spent:.2f}")
        alert_message = check_budget(total_spent, budget)

        # Send email notifications
        if "exceeded" in alert_message:
            st.error(alert_message)
            if send_email_notification(
                    "Budget Exceeded",
                    f"You have exceeded your monthly budget. Total spent: ${total_spent:.2f}",
                    user_email,
            ):
                st.success("Notification sent to your email!")
        elif "Warning" in alert_message:
            st.warning(alert_message)
            if send_email_notification(
                    "Budget Warning",
                    f"You are close to exceeding your monthly budget. Total spent: ${total_spent:.2f}",
                    user_email,
            ):
                st.success("Notification sent to your email!")
        else:
            st.success(alert_message)

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

# Display Income
st.header("Your Income")
if not income_df.empty:
    st.dataframe(income_df, use_container_width=True)
else:
    st.info("No income added yet. Start by adding income in the sidebar!")

# Expense Splitting
st.header("💸 Split Expense")
expense_to_split = st.selectbox("Select Expense to Split", expenses_df["description"])
split_amount = st.number_input("Total Amount to Split", min_value=0.0, format="%.2f")
num_people = st.number_input("Number of People", min_value=1, step=1)
if st.button("Split Expense"):
    per_person_amount = split_amount / num_people
    for i in range(num_people):
        person_name = st.text_input(f"Person {i+1} Name")
        if person_name:
            add_split_expense(expenses_df[expenses_df["description"] == expense_to_split].iloc[0]["id"], person_name, per_person_amount)
    st.success("Expense split successfully!")

# Multi-Currency Support
st.header("🌍 Multi-Currency Support")
base_currency = st.selectbox("Base Currency", ["USD", "EUR", "INR", "GBP"])
expense_currency = st.selectbox("Expense Currency", ["USD", "EUR", "INR", "GBP"])
amount_in_expense_currency = st.number_input("Amount in Expense Currency", min_value=0.0, format="%.2f")
if st.button("Convert to Base Currency"):
    amount_in_base_currency = convert_currency(amount_in_expense_currency, expense_currency, base_currency)
    st.write(f"Amount in {base_currency}: {amount_in_base_currency:.2f}")

# Debt & Loan Tracking
st.header("💳 Debt & Loan Tracking")
debt_date = st.date_input("Debt/Loan Date", datetime.today())
person_name = st.text_input("Person Name")
debt_description = st.text_input("Debt/Loan Description")
debt_amount = st.number_input("Debt/Loan Amount", min_value=0.0, format="%.2f")
debt_type = st.selectbox("Type", ["Debt", "Loan"])
if st.button("Add Debt/Loan"):
    add_debt(debt_date, person_name, debt_description, debt_amount, debt_type)
    st.success("Debt/Loan added successfully!")

# OCR-Based Receipt Upload
st.header("📄 Upload Receipt")
uploaded_file = st.file_uploader("Upload Receipt", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    extracted_text = extract_text_from_image(image)
    st.write("Extracted Text:", extracted_text)

# AI-Powered Expense Categorization
st.header("🤖 AI-Powered Categorization")
if not expenses_df.empty:
    model, vectorizer = train_expense_categorizer(expenses_df)
    description = st.text_input("Enter Expense Description")
    if description:
        predicted_category = predict_category(model, vectorizer, description)
        st.write(f"Predicted Category: {predicted_category}")