import os
import RPi.GPIO as GPIO
import time
from datetime import datetime


logfile = open("/home/pi/GarageWeb/static/log.txt","a")
logfile.write(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))
logfile.close()
print(datetime.now().strftime("     Program Starting -- %Y/%m/%d -- %H:%M  -- Hello! \n"))

print " Control + C to exit Program"

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

PreviousStatus = -1 # -1 = unknown, 0 = open, 1 = closed

try:
    while 1 >= 0:
        time.sleep(1)

        if GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH and PreviousStatus > -1:  #Door Status is Unknown
            PreviousStatus = -1
            logfile = open("/home/pi/GarageWeb/static/log.txt","a")
            logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Opening/Closing \n"))
            logfile.close()
            print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Opening/Closing \n"))
            while GPIO.input(16) == GPIO.HIGH and GPIO.input(18) == GPIO.HIGH:
                time.sleep(.5)
        else:
            if GPIO.input(16) == GPIO.LOW and PreviousStatus != 1:  #Door is Closed
                PreviousStatus = 1
                logfile = open("/home/pi/GarageWeb/static/log.txt","a")
                logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Closed \n"))
                logfile.close()
                print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Closed"))

            if GPIO.input(18) == GPIO.LOW and PreviousStatus != 0:  #Door is Open
                PreviousStatus = 0
                logfile = open("/home/pi/GarageWeb/static/log.txt","a")
                logfile.write(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Open \n"))
                logfile.close()
                print(datetime.now().strftime("%Y/%m/%d -- %H:%M:%S  -- Door Open"))

except KeyboardInterrupt:
    logfile = open("/home/pi/GarageWeb/static/log.txt","a")
    logfile.write(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
    logfile.close()
    print(datetime.now().strftime("     Log Program Shutdown -- %Y/%m/%d -- %H:%M  -- Goodbye! \n"))
    GPIO.cleanup()