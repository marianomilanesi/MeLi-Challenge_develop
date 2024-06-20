import guardar_db

def main():
    databases_json_path = 'databases.json'
    owners_csv_path = 'owners.csv'
    managers_csv_path = 'managers.csv'

    guardar_db.crear_tablas()
    guardar_db.insertar_datos(databases_json_path, owners_csv_path, managers_csv_path)
    guardar_db.enviar_emails()

if __name__ == "__main__":
    main()
