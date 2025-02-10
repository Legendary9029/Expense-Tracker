from forex_python.converter import CurrencyRates
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from PIL import Image
import pytesseract
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


# Validate expense input
def validate_expense(date, category, description, amount):
    if not date or not category or not amount:
        return False, "Date, category, and amount are required."
    if amount <= 0:
        return False, "Amount must be greater than 0."
    return True, ""


# Check budget
def check_budget(total_spent, budget):
    if total_spent > budget:
        return "You have exceeded your budget!"
    elif total_spent >= 0.8 * budget:
        return "Warning: You are close to exceeding your budget!"
    else:
        return "You are within your budget."


# Convert currency
def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    return c.convert(from_currency, to_currency, amount)


# Train expense categorizer
def train_expense_categorizer(expenses_df):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(expenses_df["description"])
    y = expenses_df["category"]
    model = MultinomialNB()
    model.fit(X, y)
    return model, vectorizer


# Predict category
def predict_category(model, vectorizer, description):
    X = vectorizer.transform([description])
    return model.predict(X)[0]


# Extract text from image (OCR)
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)


# Send email notification


# Load environment variables from .env file
load_dotenv()


def send_email_notification(subject, message, to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        print("Email credentials not set! Please update the `.env` file.")
        return False

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
