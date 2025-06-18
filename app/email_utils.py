import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_otp_email(to_email, otp):
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    if not sender_email or not sender_password:
        raise ValueError("Missing SENDER_EMAIL or SENDER_PASSWORD in environment variables.")

    subject = "Your OTP Code for Password Reset"
    body = f"Hi,\n\nYour OTP code is: {otp}\n\nUse this to reset your password.\n\nThanks!"

    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = to_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(em)
