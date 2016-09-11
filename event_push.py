import time
from pyapns import configure, provision, notify

token_hex = '6bd41c0401081a199185f7dee4caa2ac5ff34a5133fb6dc6d07500037fe0a742'

def send_notif(message="", silent=True): 
    configure({'HOST': 'http://localhost:7077/'})
    provision('BeTherePush', open('ck.pem').read(), 'sandbox')
    if silent:
        notify('BeTherePush', token_hex, {'aps':{'content-available': '1'}})
    else:
        notify('BeTherePush', token_hex, {'aps':{'alert': message}})


if __name__ == "__main__":
    send_notif("this should be silent")