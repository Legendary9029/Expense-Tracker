def validate_expense(date, category, description, amount):
    if not date or not category or not amount:
        return False, "Date, category, and amount are required."
    if amount <= 0:
        return False, "Amount must be greater than 0."
    return True, ""