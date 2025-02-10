# Expense Tracker 🤑

**Expense Tracker** is a web-based application built using **Streamlit** that helps you track and manage your expenses. It provides a wide range of features, including expense tracking, income tracking, recurring expenses, multi-currency support, debt/loan tracking, OCR-based receipt upload, AI-powered categorization, and smart notifications.

---

## Features ✨

### **Core Features**
- **Add Expenses**: Input date, category, description, and amount.
- **View Expenses**: Display all expenses in a table.
- **Categorize Expenses**: Group expenses by categories (e.g., Food, Transport, Entertainment).
- **Visualizations**: Charts for monthly spending and category-wise breakdown.
- **Filter Expenses**: Filter by date range, category, or amount.
- **Export Data**: Export expenses to CSV or Excel.
- **Budget Tracking**: Set a budget and track spending against it.
- **Edit/Delete Expenses**: Modify or remove existing entries.

### **New Features**
- **Recurring Expenses**: Set up recurring expenses (e.g., rent, subscriptions).
- **Income Tracking**: Track income sources and calculate savings.
- **Expense Splitting**: Split an expense with friends or family.
- **Multi-Currency Support**: Input expenses in different currencies and convert them to a base currency.
- **Debt & Loan Tracking**: Track money borrowed/lent and set repayment reminders.
- **OCR-Based Receipt Upload**: Extract expense details from uploaded receipts.
- **AI-Powered Expense Categorization**: Automatically categorize expenses using AI/ML.
- **Smart Notifications & Alerts**: Receive email notifications when you exceed or approach your budget.
- **Dark Mode**: Toggle between light and dark themes.

---

## Technologies Used 🛠️

- **Frontend**: Streamlit
- **Backend**: Python (Pandas, SQLite)
- **Visualization**: Matplotlib, Seaborn
- **Database**: SQLite
- **AI/ML**: Scikit-learn
- **OCR**: pytesseract
- **Email Notifications**: smtplib

---

## Installation and Setup 🚀

Follow these steps to set up the project on your local machine.

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker
   ```

2. **Create a Virtual Environment**:
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     ```
   - On Windows:
     ```bash
     python -m venv venv
     ```

3. **Activate the Virtual Environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Email Credentials Securely**:
   - Create a `.env` file in the project root directory:
     ```
     EMAIL_USER=your-email@gmail.com
     EMAIL_PASS=your-email-password
     ```
   - **Ensure the `.env` file is added to `.gitignore`** to prevent exposing credentials:
     ```
     # Ignore environment variables file
     .env
     ```
   - The application will automatically load the credentials using `python-dotenv`.

6. **Run the Application**:
   ```bash
   cd frontend
   streamlit run app.py
   ```

7. **Access the Application**:
   Open your browser and go to `http://localhost:8501`.

---

## Usage Guide 📚

### Adding an Expense
1. Open the sidebar by clicking the **>** button in the top-left corner.
2. Fill in the date, category, description, and amount.
3. Click **Add Expense**.

### Adding Recurring Expenses
1. In the sidebar, fill in the start date, end date (optional), category, description, amount, and frequency.
2. Click **Add Recurring Expense**.

### Adding Income
1. In the sidebar, fill in the income date, source, description, and amount.
2. Click **Add Income**.

### Viewing Expenses
- The main page displays a table of all expenses.
- Use the **Filter Expenses** section to filter by date range, category, or amount.

### Visualizations
- View **Monthly Spending** and **Category-wise Breakdown** charts on the main page.

### Exporting Data
- Click **Export to CSV** or **Export to Excel** to download your expense data.

### Budget Tracking
- Set a monthly budget in the **Budget Tracking** section.
- The app will display your total spending and remaining budget.
- You will receive email notifications if you exceed or approach your budget.

### Splitting Expenses
1. Select an expense to split.
2. Enter the total amount to split and the number of people.
3. Provide the names of the people involved.
4. Click **Split Expense**.

### Multi-Currency Support
1. Select the base currency and expense currency.
2. Enter the amount in the expense currency.
3. Click **Convert to Base Currency**.

### Debt & Loan Tracking
1. Fill in the debt/loan date, person name, description, amount, and type.
2. Click **Add Debt/Loan**.

### OCR-Based Receipt Upload
1. Upload a receipt image (PNG, JPG, JPEG).
2. The app will extract text from the receipt and display it.

### AI-Powered Categorization
1. Enter an expense description.
2. The app will predict the category automatically.

### Dark Mode
- Toggle **Dark Mode** in the sidebar to switch between light and dark themes.

---

## Project Structure 📂

```
expense_tracker/
│
├── backend/
│   ├── __init__.py
│   ├── database.py       # Handles database operations
│   ├── expenses.py       # Handles expense-related logic
│   └── utils.py          # Utility functions (e.g., data validation, notifications)
│
├── app.py                # Streamlit UI and interaction
│
├── venv/                 # Virtual environment folder
├── .env                  # Stores email credentials (not pushed to GitHub)
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

---

## Contributing 🤝

Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License 📝

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact 📧

For any questions or feedback, feel free to reach out:
- **Gmail** - [adityasinha1304@gmail.com](mailto:adityasinha1304@gmail.com)
- **GitHub**: [Legendary9029](https://github.com/legendary9029)

---

Enjoy tracking your expenses! 💸

