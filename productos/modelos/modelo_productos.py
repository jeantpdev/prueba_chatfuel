from librerias import *
from utils import *
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
from google.oauth2 import service_account
import json

class Formulario():  

    def leer_credenciales(self, credentials_file):
        try:
            with open(credentials_file, 'r') as file:
                credenciales = json.load(file)  # Cambiar a json.load para leer JSON
            if not credenciales:
                print("El archivo de credenciales está vacío o no se pudo leer correctamente.")
            return credenciales
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el archivo JSON de credenciales: {e}")
            return None
        except Exception as e:
            print(f"Error al leer el archivo de credenciales: {e}")
            return None

    def obtener_datos(self):
        try:
            datos = request.get_json()
            print(datos)
            return datos
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            return None

    def configurar_credenciales(self, SCOPES, CREDENTIALS_FILE_PATH):
        try:
            # Verificar si el archivo de credenciales existe
            if not os.path.exists(CREDENTIALS_FILE_PATH):
                print(f"El archivo de credenciales no se encuentra en la ruta: {CREDENTIALS_FILE_PATH}")
                return None

            # Cargar las credenciales de la cuenta de servicio desde el archivo JSON
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE_PATH, scopes=SCOPES)
            return creds
        except Exception as e:
            print(f"Error al configurar las credenciales de la cuenta de servicio: {e}")
            return None

    def crear_evento(self, service, datos):
        evento = {
            'summary': datos["summary"],
            'location': datos["location"],
            'description': datos["description"],
            'start': {
                'dateTime': datos["start_dateTime"],
                'timeZone': datos["start_timeZone"],
            },
            'end': {
                'dateTime': datos["end_dateTime"],
                'timeZone': datos["end_timeZone"],
            }
        }
        try:
            evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
            print('Evento creado: %s' % (evento_creado.get('htmlLink')))
            return evento_creado.get('htmlLink')
        except Exception as e:
            print('Ocurrió un error al crear el evento: %s' % e)
            return None

    def recibir_datos(self):
        datos = self.obtener_datos()
        if datos is None:
            return jsonify({"mensaje": "Error al obtener los datos"}), 500
        
        print(datos["summary"])
        
        # datos["summary"] = "Reunión de Proyecto"
        # datos["location"] = "Oficina Central"
        # datos["description"] = "Revisión del progreso del proyecto"
        # datos["start_dateTime"] = "2025-01-21T16:55:00"
        # datos["start_timeZone"] = "America/Los_Angeles"
        # datos["end_dateTime"] = "2025-01-21T16:59:00"
        # datos["end_timeZone"] = "America/Los_Angeles"
        
        # Verificar que todos los campos necesarios estén presentes
        required_fields = ["summary", "location", "description", "start_dateTime", "start_timeZone", "end_dateTime", "end_timeZone"]
        missing_fields = [field for field in required_fields if field not in datos]
        
        if missing_fields:
            return jsonify({"mensaje": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CREDENTIALS_FILE_PATH = '/etc/secrets/client_secrets_real'
        
        creds = self.configurar_credenciales(SCOPES, CREDENTIALS_FILE_PATH)
        service = build('calendar', 'v3', credentials=creds)

        evento_link = self.crear_evento(service, datos)
        if evento_link:
            return jsonify({"mensaje": "Datos recibidos correctamente", "nombre": datos.get("nombre"), "evento": evento_link}), 200
        else:
            return jsonify({"mensaje": "Datos recibidos correctamente, pero ocurrió un error al crear el evento", "nombre": datos.get("nombre")}), 200