import smtplib
from email.mime.text import MIMEText

SMTP_EMAIL = "mfsi.garimas@gmail.com"
SMTP_PASSWORD = "Mindfire@1011"

def send_email(to_email: str, reset_link: str):
    msg = MIMEText(f"Click to reset password:\n{reset_link}")
    msg["Subject"] = "Password Reset"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)