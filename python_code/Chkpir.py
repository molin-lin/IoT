import RPi.GPIO as GPIO
import time
from photo_shot import take_shot

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin


def chk(x):
    count = 0
    flag = False
    datetime_str =""
    while (count < 2 * x) and flag == False :
        i=GPIO.input(11)
        count = count + 1
        if i==0:                 #When output from motion sensor is LOW
            print ("No intruders",i)
            GPIO.output(3, 0)  #Turn OFF LED
            time.sleep(0.5)
        elif i==1:               #When output from motion sensor is HIGH
            print ("Intruder detected",i)
            GPIO.output(3, 1)  #Turn ON LED
            time.sleep(0.5)
            flag = True
            datetime_str=take_shot(x)
            GPIO.output(3, 0)  #Turn OFF LED
    return (flag,datetime_str)

print(chk(5))
