import os

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')

client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="[TEST] The garage door is either open or cannot be detected. Go check it!",
                     from_=os.getenv('TWILIO_FROM_PHONE', ''),
                     to_=os.getenv('TWILIO_TO_PHONE1', ''),
                 )

print(message.sid)

message = client.messages \
                .create(
                     body="[TEST] The garage door is either open or cannot be detected. Go check it!",
                     from_=os.getenv('TWILIO_FROM_PHONE', ''),
                     to_=os.getenv('TWILIO_TO_PHONE2', ''),
                 )

print(message.sid)