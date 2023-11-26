import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL')
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')

MAX_BACKGROUND_WORKERS = 4