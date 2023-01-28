from datetime import datetime, timedelta
from threading import Thread
from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import threading

cred = credentials.Certificate("pawmark-firebase-adminsdk-4g25g-1025ff6221.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


# Create an Event for notifying main thread.
callback_done = threading.Event()
# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    day_before_5_days = datetime.today() - timedelta(days=5)
    messages = []
    for change in changes:
        if change.type.name != 'ADDED':
            continue

        doc_dict = change.document.to_dict()
        date = datetime.strptime(doc_dict['date'], "%m/%d/%Y, %H:%M:%S")
        if day_before_5_days > date:
            continue
        
        print(f'{change.document.id}')
        doc_dict['id'] = change.document.id
        registration_tokens = doc_dict['device_tokens']
        title = doc_dict['title']
        message = doc_dict['message']
        doc_dict['date'] = date
        
        for token in registration_tokens:
            data = doc_dict
            del data["device_tokens"]
            messages.append(
                    messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=message,
                        
                    ),
                    data=data,
                    token=token,
                )
            )

    response = messaging.send_all(messages)
    print('{0} messages were sent successfully'.format(response.success_count))

    callback_done.set()



def start():
    col_query = db.collection(u'notifications')

    # Watch the collection query
    query_watch = col_query.on_snapshot(on_snapshot)

if __name__ == '__main__':
    print("Listening for notifications...")
    ACCEPT_THREAD = Thread(target=start)
    ACCEPT_THREAD.start()

while True:
    pass