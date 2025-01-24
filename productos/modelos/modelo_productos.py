from librerias import *
from utils import *
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path

class Formulario():  

    def leer_credenciales(self, credentials_file):
        try:
            with open(credentials_file, 'r') as file:
                credenciales = file.read()
            return credenciales
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

    def configurar_credenciales(self, SCOPES, CREDENTIALS_FILE):
        TOKEN_FILE = 'token.json'
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        return creds

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
        
        nombre = datos["nombre"]
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CREDENTIALS_FILE_PATH = r'../etc/secrets/client_secrets'
        CREDENTIALS_FILE = self.leer_credenciales(CREDENTIALS_FILE_PATH)
        
        creds = self.configurar_credenciales(SCOPES, CREDENTIALS_FILE)
        service = build('calendar', 'v3', credentials=creds)

        evento_link = self.crear_evento(service, datos)
        if evento_link:
            return jsonify({"mensaje": "Datos recibidos correctamente", "nombre": nombre, "evento": evento_link}), 200
        else:
            return jsonify({"mensaje": "Datos recibidos correctamente, pero ocurrió un error al crear el evento", "nombre": nombre}), 200