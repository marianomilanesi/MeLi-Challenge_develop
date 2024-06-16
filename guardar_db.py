import sqlite3

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

def insertar_datos(databases, user_managers):
    conn = sqlite3.connect('databases_classification.db')
    cursor = conn.cursor()
    for db in databases:
        owner_id = db['owner_email']
        owner_email = user_managers.get(owner_id)
        manager_email = user_managers.get(owner_id)
        
        if owner_email is None or manager_email is None:
            print(f"Error: No se encontró un correo válido para el owner_id {owner_id}. Registro omitido.")
            continue
        
        cursor.execute('''
        INSERT INTO database_info (database_name, owner_email, manager_email, classification)
        VALUES (?, ?, ?, ?)
        ''', (db['database_name'], owner_email, manager_email, db['classification']))
    
    conn.commit()
    conn.close()
