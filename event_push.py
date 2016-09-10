import time
from apns import APNs, Frame, Payload

apns = APNs(use_sandbox=True, cert_file='cert.pem', key_file='key.pem')

# Send a notification
def send_notif(msg, content_available=False):
    token_hex = '6bd41c0401081a199185f7dee4caa2ac5ff34a5133fb6dc6d07500037fe0a742'
    payload = Payload(alert=msg, sound="default", content_available=False, badge=1)
    apns.gateway_server.send_notification(token_hex, payload)


if __name__ == "__main__":
    send_notif("mo' Mo, mo' problems")