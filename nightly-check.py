import os
import RPi.GPIO as GPIO
import time
from datetime import datetime

logfile = open("/home/pi/GarageWeb/static/log.txt","a")
logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Scheduled garage door status check - starting \n"))
logfile.close()

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = '***REMOVED***'
auth_token = '***REMOVED***'

if (GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH) or GPIO.input(18) == GPIO.LOW:
        logfile = open("/home/pi/GarageWeb/static/log.txt","a")
        logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Garage door is open/undefined, sending SMS \n"))
        logfile.close()
        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                             body="The garage door is either open or cannot be detected. Go check it!",
                             from_='***REMOVED***',
                             to='***REMOVED***'
                         )

        print(message.sid)

        logfile = open("/home/pi/GarageWeb/static/log.txt","a")
        logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- SMS sent \n"))
        logfile.close()
else:
        logfile = open("/home/pi/GarageWeb/static/log.txt","a")
        logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Garage is closed \n"))
        logfile.close()

logfile = open("/home/pi/GarageWeb/static/log.txt","a")
logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Scheduled garage door status check - complete \n"))
logfile.close()