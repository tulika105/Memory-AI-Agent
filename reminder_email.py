import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

msg = EmailMessage()
msg["Subject"] = "Daily Learning Reminder"
msg["From"] = os.getenv("EMAIL_USER")
msg["To"] = os.getenv("EMAIL_TO")
msg.set_content("Reminder: Please log what you learned today.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    server.send_message(msg)

print("Daily reminder email sent.")
