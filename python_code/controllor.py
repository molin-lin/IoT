#Running on Raspberry pi, coding by Molin on 2021/10/22

import RPi.GPIO as GPIO
from time import sleep
from Chkpir import chk
from DHT22 import dht_data

pin_list = [12,16,18,22,32,36,38,40]
            #A:12 #GPIO18 #B:16 #GPIO23
            #C:18 #GPIO24 #D:22 #GPIO25
            #E:32 #GPIO12 #F:36 #GPIO16
            #G:38 #GPIO20 #Err:40 #GPIO21
            
            #A,B,C,D,E,F,G,Err
seven_seg = [
            [1,1,1,1,1,1,0,0],  #number 0
            [0,1,1,0,0,0,0,0],  #number 1
            [1,1,0,1,1,0,1,0],  #number 2
            [1,1,1,1,0,0,1,0],  #number 3
            [0,1,1,0,0,1,1,0],  #number 4
            [1,0,1,1,0,1,1,0],  #number 5
            [1,0,1,1,1,1,1,0],  #number 6
            [1,1,1,0,0,0,0,0],  #number 7
            [1,1,1,1,1,1,1,0],  #number 8
            [1,1,1,1,0,1,1,0],  #number 9
            [0,0,0,0,0,0,0,0],  #reset
            [0,0,0,0,0,0,0,1]   #Error
            ]

def initial():        
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pin_list, GPIO.OUT)

def display(number):  
    GPIO.output(pin_list, seven_seg[number])

   
def is_number(nb):                  #check the type of input
    try:
        int(nb)
        return True
    except:
        return False

def control(x):        
    initial()
    nbr = x

    if (is_number(nbr)):
        nbr=int(nbr)
        if(nbr>=0 and nbr<=9):
            display(nbr)                 #Display number from 7-seg. display
        else:
            nbr =11                      #Err led
            display(nbr)
        ret_str ="Input is: " + str(nbr)
        
    else:
        if (str(nbr).lower()=="clear"):
            display(10)                  #set 7-seg display off
            ret_str="7 Segment Display RESET"    
        
        elif(str(nbr).lower()=="turnoff"): 
            for cout in range(5,-1,-1):         #count down
                display(cout)
                sleep(1)
            display(10)
            ret_str = "off" 
            
        elif(str(nbr).lower()=="turnon"): 
            display(11)
            ret_str = "on"  
        elif (str(nbr).lower()=="pir"): 
            if chk(5):
                ret_str = "感應有人" 
            else:
                ret_str = "感應無人"
        elif (str(nbr).lower()=="dht"): 
            ret_str = "現在溫濕度 : " + str(dht_data())
            
        else: 
            #display(11)                  #Err led
            ret_str=nbr
    
    #GPIO.cleanup()
    return (ret_str)
