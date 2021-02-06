import os
import pyrebase

firebase_config = {
    'apiKey': os.environ.get('API_KEY'),
    'authDomain': os.environ.get('AUTH_DOMAIN'),
    'databaseURL': os.environ.get('DATABASE_URL'),
    'projectId': os.environ.get('PROJECT_ID'),
    'storageBucket': os.environ.get('STORAGE_BUCKET'),
    'messagingSenderId': os.environ.get('MESAAGEING_ID'),
    'appId': os.environ.get('APP_ID'),
    'measurementId': os.environ.get('MEASUREMENT')
}

firebase = pyrebase.initialize_app(firebase_config)