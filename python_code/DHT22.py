#This codes referenced from https://stackoverflow.com/questions/32236588/passing-dht22-output-in-python-to-php

import Adafruit_DHT 

DHT_SENSOR = Adafruit_DHT.DHT22 
DHT_PIN = 4  # define the GPIO pin 4, Board number 7

def dht_data():
#while True:
    #Get humidity and temperature)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    hu = "相對溼度 = {:0.2f}%".format(humidity)
    te = "攝氏 = {:0.2f}°C".format(temperature)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.2f}*C  Humidity={1:0.2f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from HDT22 sensor")
    #time.sleep(1) 
    return te,hu
    
