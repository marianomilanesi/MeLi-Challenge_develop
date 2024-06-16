import json
import csv

def leer_datos_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def leer_datos_csv(csv_path):
    user_managers = {}
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'user_id' in row and 'user_manager' in row:
                    user_managers[row['user_id']] = row['user_manager']
                else:
                    print("Error: La cabecera del archivo CSV es incorrecta.")
    except FileNotFoundError:
        print("Error: El archivo 'users.csv' no se encuentra.")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
    return user_managers
