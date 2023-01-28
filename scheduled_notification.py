import schedule
import time
from datetime import datetime, timedelta
from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import pytz

utc=pytz.UTC

cred = credentials.Certificate("pawmark-firebase-adminsdk-4g25g-1025ff6221.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def job():
    print('checking all notifications...')
    day_before_5_days = (datetime.today() - timedelta(days=5)).replace(tzinfo=pytz.timezone('Asia/Manila'))
    docs = db.collection(u'notifications').where(u'read', u'!=', "yes").stream()

    messages = []
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
        doc_dict = doc.to_dict()
        date = datetime.strftime(doc_dict['date'], "%m/%d/%Y, %H:%M:%S")


        if day_before_5_days > doc_dict['date']:
            continue

        doc_dict['id'] = doc.id
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

    if len(messages) > 0:
        response = messaging.send_all(messages)
        print('{0} messages were sent successfully'.format(response.success_count))

    print('Done job')

schedule.every(5).seconds.do(job)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every(1).day.do(job)
# schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)