import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if available

import json

def send_email(subject, body, to_email=''):
    # Retrieve SMTP configuration from environment variables
    smtp_server = os.getenv("SMTP_SERVER", "smtp.office365.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_receiver = os.getenv("SMTP_RECEIVER")

    # Debug output to check values and their types
    print("SMTP_SERVER:", smtp_server, type(smtp_server))
    print("SMTP_PORT:", smtp_port, type(smtp_port))
    print("SMTP_USERNAME:", smtp_username, type(smtp_username))
    print("SMTP_RECEIVER:", smtp_receiver, type(smtp_receiver))
    
    # Validate that required values are provided
    if not smtp_server:
        raise ValueError("SMTP_SERVER environment variable is not set.")
    if not smtp_username:
        raise ValueError("SMTP_USERNAME environment variable is not set.")
    if not smtp_password:
        raise ValueError("SMTP_PASSWORD environment variable is not set.")
    if not smtp_receiver:
        raise ValueError("SMTP_RECEIVER environment variable is not provided.")
    
    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = smtp_username  # Sender address
    msg["To"] = smtp_receiver    # Recipient address from environment
    msg["Subject"] = str(subject)
    msg.attach(MIMEText(body, "plain"))

    try:
        # Instantiate the SMTP object with the server and port
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        
        # Create a default SSL context and start TLS
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.ehlo()
        
        # Log in and send the email
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, smtp_receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False