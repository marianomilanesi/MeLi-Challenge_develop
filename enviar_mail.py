# enviar_mail.py

import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USER = 'tu_correo'  # Aquí debes colocar tu dirección de correo
SMTP_PASSWORD = 'tu_password'  # Aquí debes colocar tu contraseña

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email enviado a {to_email}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Error de autenticación SMTP: {e}")
    except Exception as e:
        print(f"Error al enviar el email: {e}")

def enviar_emails():
    try:
        conn = sqlite3.connect('databases_classification.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT owner_email, manager_email, database_name
        FROM database_info
        WHERE classification = 'high'
        ''')
        high_classification_databases = cursor.fetchall()
        
        for db in high_classification_databases:
            owner_email, manager_email, database_name = db
            subject = f"Revalidación de Clasificación de {database_name}"
            body = f"Estimado/a,\n\nPor favor, confirme la clasificación 'high' de la base de datos {database_name} propiedad de {owner_email}.\n\nSaludos,\nEquipo de Seguridad Informática"
            send_email(manager_email, subject, body)
        
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
    finally:
        if conn:
            conn.close()
