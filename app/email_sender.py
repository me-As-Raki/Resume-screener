import smtplib
from email.message import EmailMessage

def send_email(to, subject, body):
    try:
        sender_email = "rakeshpoojary850@gmail.com"
        app_password = "zmvvppmowvnnurcp"  # Your real app password

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)

# ✅ Example usage
send_email("poojaryreshma850@gmail.com", "Test Email from Flask", "Hello! This is a test email from your Flask app.")
