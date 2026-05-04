import smtplib
from email.mime.text import MIMEText
import os

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(to_email: str, reset_link: str):
    print(to_email)
    msg = MIMEText(f"Click to reset password:\n{reset_link}")
    msg["Subject"] = "Password Reset"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)