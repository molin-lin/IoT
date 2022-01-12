#These codes as below is clone from https://github.com/miguelgrinberg/flask-video-streaming
#and create some codes with remarks behind.

#!/usr/bin/env python

import os, sys
from importlib import import_module
from __future__ import unicode_literals
from flask import Flask, render_template, Response, request, abort
from controllor import control
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

app = Flask(__name__)



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'



# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 回覆 LINE 的訊息
@handler.add(MessageEvent, message=TextMessage)
def reply_to_line(event):
    
    # functions control
    reply_text = ''
    reply_text += event.message.text
    reply_text += " has done!"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/<string:functionID>')  #Create to sumulate the controlor via GPIO, 2022/1/9, Molin
def cntl(functionID):
    message = control(functionID)
    if message=="on":
        return render_template('set_on.html')
    elif message=="off":
        return render_template('set_off.html')
    elif message=="video":
        return render_template('video.html')
    else:
        return message
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
