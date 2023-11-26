import firebase_admin
from firebase_admin import credentials, firestore_async
from backend.core.config import FIREBASE_DATABASE_URL, FIREBASE_CREDENTIALS_PATH

db = None


def initialize_firebase():
    global db
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DATABASE_URL
    })
    db = firestore_async.client()


# Connect to Firebase
def connect_to_firebase():
    initialize_firebase()
