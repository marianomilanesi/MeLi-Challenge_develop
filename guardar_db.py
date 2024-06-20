import sqlite3
import leer_procesar
import enviar_mail

def crear_tablas():
    conn = sqlite3.connect('databases_classification.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS database_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        database_name TEXT NOT NULL,
        owner_email TEXT NOT NULL,
        manager_email TEXT NOT NULL,
        classification TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insertar_datos(databases_json_path, owners_csv_path, managers_csv_path):
    databases = leer_procesar.leer_datos_json(databases_json_path)
    user_owners = leer_procesar.leer_datos_csv(owners_csv_path)
    user_managers = leer_procesar.leer_datos_csv(managers_csv_path)

    conn = sqlite3.connect('databases_classification.db')
    cursor = conn.cursor()

    for db in databases:
        owner_email = db['owner_email']
        
        # Buscar el correo del owner en user_owners
        owner_email = user_owners.get(owner_email)
        
        if owner_email is None:
            print(f"Error: No se encontró un correo válido para el owner_email {db['owner_email']}. Registro omitido.")
            continue
        
        # Buscar el manager correspondiente según el user_id del owner
        manager_user_id = owner_email[0]
        manager_email = user_managers.get(manager_user_id)

        if manager_email is None:
            print(f"Error: No se encontró un correo válido para el manager_id {manager_user_id} asociado al owner_email {db['owner_email']}. Registro omitido.")
            continue

        cursor.execute('''
        INSERT INTO database_info (database_name, owner_email, manager_email, classification)
        VALUES (?, ?, ?, ?)
        ''', (db['database_name'], owner_email[1], manager_email, db['classification']))
    
    conn.commit()
    conn.close()

def enviar_emails():
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
        enviar_mail.send_email(manager_email, subject, body)
    
    conn.close()

