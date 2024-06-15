import json
import csv
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Leer archivo JSON
with open('databases.json', 'r') as f:
    databases = json.load(f)

# Leer archivo CSV
users = {}
try:
    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'user_id' in row and 'user_manager' in row:
                users[row['user_id']] = row['user_manager']
            else:
                print("Error: La cabecera del archivo CSV es incorrecta.")
except FileNotFoundError:
    print("Error: El archivo 'users.csv' no se encuentra.")
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")

# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect('databases_classification.db')
cursor = conn.cursor()

# Crear la tabla
cursor.execute('''
CREATE TABLE IF NOT EXISTS database_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    database_name TEXT NOT NULL,
    owner_email TEXT NOT NULL,
    manager_email TEXT NOT NULL,
    classification TEXT NOT NULL
)
''')

# Insertar los datos
for db in databases:
    owner_email = db['owner_email']
    manager_email = users.get(owner_email, "unknown@example.com")
    cursor.execute('''
    INSERT INTO database_info (database_name, owner_email, manager_email, classification)
    VALUES (?, ?, ?, ?)
    ''', (db['database_name'], owner_email, manager_email, db['classification']))

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

# Configuración del servidor SMTP de Outlook
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USER = 'tucorreo@outlook.com'
SMTP_PASSWORD = 'tucontraseña'

# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect('databases_classification.db')
cursor = conn.cursor()

# Seleccionar las bases con clasificación "high"
cursor.execute('''
SELECT owner_email, manager_email, database_name
FROM database_info
WHERE classification = 'high'
''')
high_classification_databases = cursor.fetchall()

# Función para enviar email
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

# Enviar email a cada manager
for db in high_classification_databases:
    owner_email, manager_email, database_name = db
    subject = f"Revalidación de Clasificación de {database_name}"
    body = f"Estimado/a,\n\nPor favor, confirme la clasificación 'high' de la base de datos {database_name} propiedad de {owner_email}.\n\nSaludos,\nEquipo de Seguridad Informática"
    send_email(manager_email, subject, body)
    #send_email("milanesimariano@gmail.com", subject, body)

# Cerrar conexión a la base de datos
conn.close()
