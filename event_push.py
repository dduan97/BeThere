import time
from apns import APNs, Frame, Payload

apns = APNs(use_sandbox=True, cert_file='push_cert.pem', key_file='push_key.pem')

# Send a notification
def send_notif(msg):
    token_hex = '6bd41c0401081a199185f7dee4caa2ac5ff34a5133fb6dc6d07500037fe0a742'
    payload = Payload(alert=msg, sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)