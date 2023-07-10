from time import *
from grovepi import *
from pyrebase import pyrebase
from FakeDevices import *
import logging
from grove_rgb_lcd import *
from mfrc522 import SimpleMFRC522
import random

log = logging.getLogger(__name__)
writer= SimpleMFRC522()
pidevicename = "CR01"

ultrasonic_port1 = 9
ultrasonic_port2 = 13

led = 6
buzzer = 5

pinMode(ultrasonic_port1, "INPUT")
pinMode(ultrasonic_port2, "INPUT")
pinMode(led, "OUTPUT") #led lights up when parking available
pinMode(buzzer, "OUTPUT") #Access granted/denied from Rfid
setRGB(5,15,50) #red,green
reader = SimpleMFRC522()
buzzer=3
pinMode(buzzer, "OUTPUT")

config = {
    
    # school device 01
    "apiKey": "AIzaSyA-b-Fs1FWOjeN9qKuwKUZlIfUg_-6nPc0",
    "authDomain": "bait2123-202109-01-default-rtdb.asia-southeast1.firebasedatabase.app",
    "databaseURL": "https://bait2123-202109-01-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "bait2123-202109-01.appspot.com" 
    
}

config2 = {
    # iot g6 account
    "apiKey":"AIzaSyBIti5Eio-64MGYLas3WVC7HELIqg2mBVk",
    "authDomain": "bait-2123-iot-g6",
    "databaseURL": "https://bait-2123-iot-g6-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "gs://bait-2123-iot-g6.appspot.com"    
}

# own database
firebase2 = pyrebase.initialize_app(config2)
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("iot2123g6@gmail.com","2123B@iti0t")
db2 = firebase2.database()

# school database
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("bait2123.iot.01@gmail.com","BeyondEducation")
db = firebase.database()




        
        
print("Connecting to Firebase...")
#Turn on/off oled
db.child(pidevicename+"_CONTROL").update({'oledsc': str(0)})

    
def writeBuzzer(state):
    db.child(pidevicename+"_CONTROL").update({'buzzer':str(state)})
    db2.child(pidevicename+"_CONTROL").update({'buzzer':str(state)})


#Common resource default setting
db.child(pidevicename+"_CONTROL").update({
                    'buzzer': str(0),
                    'led': str(0),
                    'lcdbkB': str(0),
                    'lcdbkG': str(10),
                    'lcdbkR': str(0),
                    'lcdscr': str(1),
                    'rlyfan': str(0),
                    'oledsc': str(0),
                    'lcdtxt': str("=App is running=")})

#---------------------------RFID AUTHORIZATION-----------------------
   
stop=0
    
password=int(input('Please enter pin number: '))
lastDigit=password%10
if lastDigit==1 or lastDigit==2 or lastDigit==3:
    print('Please tap the card on RFID reader/writer')
    id, text = reader.read_sector(lastDigit) 
#             text=trim(text)
    print(f'id:{id},text:{text}\n')
    if password == int(text):
        print("Access Granted")
        db.child(pidevicename+"_CONTROL").update({'lcdtxt':str("====Welcome!====")})
        db2.child(pidevicename+"_CONTROL").update({'lcdtxt':str("====Welcome!====")})
        sleep(5)
    else:
        print("Access Denied")
        db.child(pidevicename+"_CONTROL").update({
            'lcdtxt':str("=Access Denied!="),
            'lcdbkR': str(10),
            'lcdbkB': str(0),
            'lcdbkG': str(0)})
        db2.child(pidevicename+"_CONTROL").update({
            'lcdtxt':str("=Access Denied!="),
            'lcdbkR': str(10),
            'lcdbkB': str(0),
            'lcdbkG': str(0)})
        writeBuzzer(1)
        sleep(2)
        writeBuzzer(0)
        sleep(5)
        stop=1
        
                
else:
    print("Invalid password.")
    stop=1

            
    
while(stop==0):
    try:        
        # sensor
        sleep(2.0)
        distance1 = ultrasonicRead(ultrasonic_port1)
        distance2 = ultrasonicRead(ultrasonic_port2) 

        print('Parking Distance 1: ', distance1, ' m')
        print('Parking Distance 2: ', distance2, ' m')
        #Push data to Firebase
        data = {"ult1":str(distance1),"ult2":str(distance2)}
        db.child(pidevicename+"_CONTROL").update(data)
        db2.child(pidevicename+"_CONTROL").update(data)


        





#------------------------------------FINDING PARKING AVAILABILITY-----------------

        
        #conditions
        if (distance1 <= 100 and distance2>100):
            db.child(pidevicename+"_CONTROL").update({
                    'relay1':str(0),#green
                    'relay2':str(1),
                    'lcdbkB': str(0),
                    'lcdbkG': str(10),
                    'lcdbkR': str(0),
                    'lcdscr': str(1),
                    'lcdtxt': str("1 Slot Available"),
                    'status':str('1B')})   
            print("Parking slot available")
            db2.child("smart_park").update({'status': str('1B')})
            
        elif(distance1 > 100 and distance2 <= 100):
            db.child(pidevicename+"_CONTROL").update({
                    'relay1':str(1), #green
                    'relay2':str(0), 
                    'lcdbkB': str(0),
                    'lcdbkG': str(10),
                    'lcdbkR': str(0),
                    'lcdscr': str(1),
                    'lcdtxt': str("1 Slot Available"),
                    'status':str('1A')})  
            print("Parking slot available")
            db2.child("smart_park").update({'status': str('1A')})
        elif(distance1 > 50 and distance2 > 50):
            db.child(pidevicename+"_CONTROL").update({
                    'relay1':str(1), #green
                    'relay2':str(1),
                    'lcdbkB': str(0),
                    'lcdbkG': str(10),
                    'lcdbkR': str(0),
                    'lcdscr': str(1),
                    'lcdtxt': str("2 Slots Available"),
                    'status':str('BothYes')})
            db2.child("smart_park").update({'status': str('BothYes')})
        else:
            db.child(pidevicename+"_CONTROL").update({
                    'buzzer': str(0),
                    'relay1':str(0),#red
                    'relay2':str(0),
                    'lcdbkB': str(0),
                    'lcdbkG': str(0),
                    'lcdbkR': str(10),
                    'lcdscr': str(1),
                    'rlyfan': str(0),
                    'lcdtxt': str("==Parking full=="),
                    'status':str('BothNo')})
            db2.child("smart_park").update({'status': str('BothNo')})
            
        
#------------------------------------DISPLAY PARKING SPOT-----------------
            
            
        lcdText= db.child(pidevicename+"_CONTROL").get()
        for value in lcdText.each():
            if value.key()=='status':
                dataValue = value.val()
                if dataValue == '1A':
                    db.child(pidevicename+"_CONTROL").update({'lcdtxt': str("Parking spot: 1A")})
                elif dataValue == '1B':
                    db.child(pidevicename+"_CONTROL").update({'lcdtxt': str("Parking spot: 1B")})
                elif dataValue=='BothYes':
                    db.child(pidevicename+"_CONTROL").update({'lcdtxt': str("ParkingAvailable")})
                elif dataValue=='BothNo':
                    db.child(pidevicename+"_CONTROL").update({'lcdtxt': str("==Parking full==")})



    except KeyboardInterrupt:
        break
    except TypeError:
        print("Type Error occurs.")
        break
    except IOError:
        print("I/O Error occurs.")
        break
