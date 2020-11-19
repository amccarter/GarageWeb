import os
import time
import timeit
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import ssl
from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_phone = os.getenv('TWILIO_FROM_PHONE')
to_phone_1 = os.getenv('TWILIO_TO_PHONE1')

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)  # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(18, GPIO.IN, GPIO.PUD_UP) # set up pin ?? (one of the above listed pins) as an input with a pull-up resistor
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
        print("Garage is Opening/Closing")
        return app.send_static_file('Question.html')
    else:
        if GPIO.input(16) == GPIO.LOW:
            print ("Garage is Closed")
            return app.send_static_file('Closed.html')
        if GPIO.input(18) == GPIO.LOW:
            print ("Garage is Open")
            return app.send_static_file('Open.html')

@app.route('/status')
def status():
    doorstatus = "unknown"
    if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
        doorstatus = "unknown"
    elif GPIO.input(16) == GPIO.LOW:
        doorstatus = "closed"
    elif GPIO.input(18) == GPIO.LOW:
        doorstatus = "open"
            
    return jsonify(
        status=doorstatus
    )

@app.route('/trigger', methods=['POST'])
def trigger():
    passcode = request.get_json()['passcode']
    if passcode == "12345678":  # 12345678 is the Password that Opens Garage Door (Code if Password is Correct)
        logfile = open("/home/pi/GarageWeb/static/log.txt","a")
        logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Passcode entered, door Opening/Closing \n"))
        logfile.close()
        
        GPIO.output(7, GPIO.LOW)
        time.sleep(1)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(2)

    if passcode != "12345678":  # 12345678 is the Password that Opens Garage Door (Code if Password is Incorrect)
        if passcode == "":
            passcode = "NULL"
        print("Incorrect garage Code Entered: " + passcode)
        logfile = open("/home/pi/GarageWeb/static/log.txt","a")
        logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Invalid passcode entered: " + passcode + " \n"))
        logfile.close()

@app.route('/getlogs', methods=['GET'])
def getlogs():
    with open('/home/pi/GarageWeb/static/log.txt', 'r') as f:
        return jsonify(
            log = f.read()
       )

@app.route('/Garage', methods=['GET', 'POST'])
def Garage():
    name = request.form['garagecode']
    if name == "12345678":  # 12345678 is the Password that Opens Garage Door (Code if Password is Correct)
        GPIO.output(7, GPIO.LOW)
        time.sleep(1)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(2)

        if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
            print("Garage is Opening/Closing")
            return app.send_static_file('Question.html')
        else:
            if GPIO.input(16) == GPIO.LOW:
                print ("Garage is Closed")
                return app.send_static_file('Closed.html')
            if GPIO.input(18) == GPIO.LOW:
                print ("Garage is Open")
                return app.send_static_file('Open.html')

    if name != "12345678":  # 12345678 is the Password that Opens Garage Door (Code if Password is Incorrect)
        if name == "":
            name = "NULL"
        print("Garage Code Entered: " + name)
        if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
            print("Garage is Opening/Closing")
            return app.send_static_file('Question.html')
        else:
            if GPIO.input(16) == GPIO.LOW:
                print ("Garage is Closed")
                return app.send_static_file('Closed.html')
            if GPIO.input(18) == GPIO.LOW:
                print ("Garage is Open")
                return app.send_static_file('Open.html')

@app.route('/receivesms', methods=['POST'])
def receivesms():
    sid = request.form.get('AccountSid')
    smsbody = request.form.get('Body')

    if sid != account_sid:
        sid  = 'NULL'
        response = jsonify({'message': 'Access denied'})

        return response, 401
    try:
        client = Client(account_sid, auth_token)

        message = client.messages \
        .create(
            body=smsbody,
            from_=from_phone,
            to=to_phone_1
        )

        print(message.sid)

        msgresponse = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'

        return msgresponse, 200

    except Exception as e:
        response = jsonify({'message': str(e)})
        return response, 500

@app.route('/stylesheet.css')
def stylesheet():
    return app.send_static_file('stylesheet.css')

@app.route('/Log')
def logfile():
    with open('/home/pi/GarageWeb/static/log.txt', 'r') as f:
        return render_template('log.html', text=f.read())

@app.route('/images/<picture>')
def images(picture):
    return app.send_static_file('images/' + picture)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ctx.load_cert_chain('/home/pi/GarageWeb/cert.pem', '/home/pi/GarageWeb/key.pem')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, ssl_context=ctx)