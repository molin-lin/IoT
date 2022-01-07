from flask import Flask
from Chkpir import chk
from seven_segment_control import control

app = Flask(__name__)

@app.route("/")
def hello():
    return "Message from Raspberry Pi [Molin]"

@app.route("/PIR")
def PIR():
    if chk(5):
    #if True:
        return "Somebody home"
    else:
        return "Nobody home"
        
@app.route("/control")
def cntl():
    message = control("bye")
    return message
        
@app.route("/CAM")
def CAM():
    return "message"    
        

@app.route("/<message>")
def echo(message):
    return (message + '~') * 3

if __name__ == '__main__':
    app.run(host='0.0.0.0')
