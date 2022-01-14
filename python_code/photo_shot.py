#referenced https://picamera.readthedocs.io/en/release-1.10/api_camera.html

from picamera import PiCamera
from time import sleep
import datetime

def take_shot(x):
    datetime_str=""
    camera = PiCamera()
    try:
        camera.start_preview()
        sleep(x)
        datetime_str = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
        camera.capture('/home/pi/Pictures/%s.jpg'%(datetime_str))
        camera.stop_preview()
    finally:
        camera.close()
    return (datetime_str)
