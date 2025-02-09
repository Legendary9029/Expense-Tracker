# Expense Tracker 🤑

**Expense Tracker** is a web-based application built using **Streamlit** that helps you track and manage your expenses. It provides features like adding expenses, categorizing them, visualizing spending patterns, filtering expenses, and exporting data.

---

## Features ✨

- **Add Expenses**: Input date, category, description, and amount.
- **View Expenses**: Display all expenses in a table.
- **Categorize Expenses**: Group expenses by categories (e.g., Food, Transport, Entertainment).
- **Visualizations**: Charts for monthly spending and category-wise breakdown.
- **Filter Expenses**: Filter by date range, category, or amount.
- **Export Data**: Export expenses to CSV or Excel.
- **Budget Tracking**: Set a budget and track spending against it.
- **Edit/Delete Expenses**: Modify or remove existing entries.

---

## Technologies Used 🛠️

- **Frontend**: Streamlit
- **Backend**: Python (Pandas, SQLite)
- **Visualization**: Matplotlib, Seaborn
- **Database**: SQLite

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

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**:
   Open your browser and go to `http://localhost:8501`.

---

## Usage Guide 📖

### Adding an Expense
1. Open the sidebar by clicking the **>** button in the top-left corner.
2. Fill in the date, category, description, and amount.
3. Click **Add Expense**.

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

### Editing/Deleting Expenses
- Enter the index of the expense you want to edit or delete.
- Click **Edit Expense** or **Delete Expense**.

---

## Project Structure 📂

```
expense_tracker/
│
├── backend/
│   ├── __init__.py
│   ├── database.py       # Handles database operations
│   ├── expenses.py       # Handles expense-related logic
│   └── utils.py          # Utility functions (e.g., data validation)
│── app.py            # Streamlit UI and interaction
├── venv/                  # Virtual environment folder
├── requirements.txt       # Dependencies
└── .gitignore             # Git ignore file
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

## License 📄

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙏

- Built with ❤️ using **Streamlit**.
- Inspired by personal finance management tools.

---

## Contact 📧

For any questions or feedback, feel free to reach out:
- **Gmail** - [adityasinha1304@gmai.com](mailto:adityasinha1304@gmai.com)
- **GitHub**: [Legendary9029](https://github.com/legendary9029)

---

Enjoy tracking your expenses! 💸
