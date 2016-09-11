import time
from pyapns import configure, provision, notify
import os

token_hex = '6bd41c0401081a199185f7dee4caa2ac5ff34a5133fb6dc6d07500037fe0a742'

def send_notif(message="", silent=True, event_id=None): 
    configure({'HOST': 'http://localhost:7077/'})
    provision('BeTherePush', os.environ["PEMPEM"], 'sandbox')
    if silent:
        if event_id:
            notify('BeTherePush', token_hex, {'aps':{'content-available': '1'}, 'event_id': event_id})
        else:
            notify('BeTherePush', token_hex, {'aps':{'content-available': '1'}})
    else:
        notify('BeTherePush', token_hex, {'aps':{'alert': message}})


if __name__ == "__main__":
    send_notif(message="this should not be silent", silent=False)