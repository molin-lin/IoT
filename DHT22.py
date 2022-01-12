# codes
import Adafruit_DHT 

DHT_SENSOR = Adafruit_DHT.DHT22 
DHT_PIN = 4  (定義針腳為 4, Board 編號 7)

#while True:
    #讀取溫溼度資料到兩個變數(humidity,temperature)
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    if humidity is not None and temperature is not None:
        print("Temp={0:0.2f}*C  Humidity={1:0.2f}%".format(temperature, humidity))
    else:
        print("Failed to retrieve data from HDT22 sensor")
    time.sleep(1)