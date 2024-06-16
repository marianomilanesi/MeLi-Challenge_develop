import leer_procesar
import guardar_db
import enviar_mail

# Leer datos
databases = leer_procesar.leer_datos_json('databases.json')
user_managers = leer_procesar.leer_datos_csv('users.csv')

# Guardar en base de datos
guardar_db.crear_tablas()
guardar_db.insertar_datos(databases, user_managers)

# Enviar emails
enviar_mail.enviar_emails()
