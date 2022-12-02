import pyperclip
import time, threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from gps_tcp_server import LOGGER

DATABASE = None
DB_REF = None
LONGITUDE_KEY = 'longitude'
LATITUDE_KEY = 'latitude'
IMEI = '359339077128046'


def update_db_ref(imei):
    try:
        if DATABASE is None:
            LOGGER('database', 'database_log.txt', 'Database is not initialized! run init_firebase() first!')
            return

        global DB_REF
        DB_REF = DATABASE.collection('locations').document(imei)
    except Exception as e:
        LOGGER('database', 'database_log.txt', e)
    LOGGER('database', 'database_log.txt', 'db_ref initialized')

def init_firebase():
    cred = credentials.Certificate("pawmark-firebase-adminsdk-4g25g-1025ff6221.json")
    firebase_admin.initialize_app(cred)
    global DATABASE
    DATABASE = firestore.client()
    update_db_ref(IMEI)
    scrape()


def write_location_to_database(location):
    try:
        if DB_REF is None:
            return
        DB_REF.set({
            LONGITUDE_KEY : location[LONGITUDE_KEY],
            LATITUDE_KEY : location[LATITUDE_KEY],
            'date' : firestore.SERVER_TIMESTAMP
        }, merge=True)
    except Exception as e:
        LOGGER('database', 'database_log.txt', e)
    LOGGER('database', 'database_log.txt', 'Write location completed')


def scrape():
    clip_text = pyperclip.paste()
    if clip_text is None:
        start_thread()
        return
    clip_text_split = clip_text.split(',')
    if len(clip_text_split) != 2:
        start_thread()
        return
    try:
        longitude = float(clip_text_split[0])
        latitude = float(clip_text_split[1])

        write_location_to_database({LONGITUDE_KEY: longitude, LATITUDE_KEY: latitude})
        print(longitude)
        print(latitude)
    except ValueError:
        pass

    start_thread()
    

def start_thread():
    threading.Timer(20, scrape).start()

init_firebase()
