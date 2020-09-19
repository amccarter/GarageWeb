import os

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_phone = os.environ['TWILIO_FROM_PHONE']
to_phone_1 = os.environ['TWILIO_TO_PHONE1']
to_phone_2 = os.environ['TWILIO_TO_PHONE2']

client = Client(account_sid, auth_token)

message = client.messages \
    .create(
        body="[TEST] The garage door is either open or cannot be detected. Go check it!",
        from_=from_phone,
        to=to_phone_1
    )

print(message.sid)

message = client.messages \
    .create(
        body="[TEST] The garage door is either open or cannot be detected. Go check it!",
        from_=from_phone,
        to=to_phone_2
    )

print(message.sid)