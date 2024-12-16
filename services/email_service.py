import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import GMAIL_USER, GMAIL_PASSWORD, DEST_EMAIL

def send_email(content, subject):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = DEST_EMAIL
        msg['Subject'] = f"Análisis de documento: {subject}"
        
        msg.attach(MIMEText(content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)
            
        logging.info("Email enviado correctamente")
    except Exception as e:
        logging.error(f"Error en send_email: {str(e)}")
        raise
