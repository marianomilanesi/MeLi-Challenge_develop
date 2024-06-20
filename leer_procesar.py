import json
import csv

def leer_datos_json(json_path):
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{json_path}' no se encuentra.")
    except Exception as e:
        print(f"Error al leer el archivo JSON '{json_path}': {e}")
    return []

def leer_datos_csv(csv_path):
    user_data = {}
    try:
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'user_id' in row and 'user_manager' in row:
                    user_data[row['user_id']] = row['user_manager']
                else:
                    print(f"Error: La cabecera del archivo CSV '{csv_path}' es incorrecta.")
    except FileNotFoundError:
        print(f"Error: El archivo '{csv_path}' no se encuentra.")
    except Exception as e:
        print(f"Error al leer el archivo CSV '{csv_path}': {e}")
    return user_data
