import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from jinja2 import Environment, FileSystemLoader

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
LOGO_URL = f"{os.getenv('DOMAIN')}/{os.getenv('LOGO')}"
print(LOGO_URL)
env = Environment(loader=FileSystemLoader("templates"))

def render_email(reset_link: str):
    template = env.get_template("reset-password.html")
    return template.render(reset_link=reset_link, logo_url=LOGO_URL)

def send_email(to_email: str, reset_link: str):

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Password Reset"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    html_content = render_email(reset_link)

    text_content = f"Reset your password: {reset_link}"

    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)