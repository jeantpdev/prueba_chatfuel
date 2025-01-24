from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path

# Configura las credenciales
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Archivo de credenciales de OAuth 2.0
CREDENTIALS_FILE = r'C:\Users\jtrujillo\Desktop\Scripts\Otros\Otros\API PRUEBA\Google\Google Keys\client_secret_591857227670-2h9lc2u68lp50khmd1k5n3ncevjfljq9.apps.googleusercontent.com.json'

# Token de acceso almacenado
TOKEN_FILE = 'token.json'

# Autenticación con OAuth 2.0
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

service = build('calendar', 'v3', credentials=creds)

# Datos de la cita
evento = {
    'summary': 'Reunión de Proyecto',
    'location': 'Oficina Central',
    'description': 'Revisión del progreso del proyecto',
    'start': {
        'dateTime': '2025-01-21T16:55:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2025-01-21T16:59:00',
        'timeZone': 'America/Los_Angeles',
    }
}

try:
    evento_creado = service.events().insert(calendarId='primary', body=evento).execute()
    print('Evento creado: %s' % (evento_creado.get('htmlLink')))
except Exception as e:
    print('Ocurrió un error al crear el evento: %s' % e)