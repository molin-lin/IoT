from picamera import PiCamera
from time import sleep

camera = PiCamera()

#camera.rotation = 180  if image is upside-down

camera.start_preview()
sleep(5)
camera.stop_preview()
