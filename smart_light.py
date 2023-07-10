from time import *
from grovepi import *
from pyrebase import pyrebase
from FakeDevices import *
from grove_rgb_lcd import *

light_sensor = 2
led = 3
pidevicename = "CR01"

pinMode(light_sensor, "INPUT")
pinMode(led, "OUTPUT")

config = {
    
    # school device 01
    "apiKey": "AIzaSyA-b-Fs1FWOjeN9qKuwKUZlIfUg_-6nPc0",
    "authDomain": "bait2123-202109-01-default-rtdb.asia-southeast1.firebasedatabase.app",
    "databaseURL": "https://bait2123-202109-01-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "bait2123-202109-01.appspot.com" 
    
}
pidevicename = "CR01"
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

#school database
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("bait2123.iot.01@gmail.com","BeyondEducation")
db = firebase.database()

while True:
    try:
        time.sleep(1)
        light = analogRead(light_sensor)
        
        data2 = {
            'light_sensor': str(light)}
        
        db2.child('Smart_Light').update(data2)

        
        if light < 500:
            digitalWrite(led, 1)
            print("Light is turn on")
            db.child(pidevicename+"_CONTROL").update({
                    'buzzer': str(0),
                    'led': str(0),
                    'lcdbkB': str(0),
                    'lcdbkG': str(0),
                    'lcdbkR': str(5),
                    'lcdscr': str(1),
                    'rlyfan': str(0),
                    'relay1': str(1),
                    'lcdtxt':str("hello")})
            
        else:
            digitalWrite(led, 0)
            print("Light is turn off")
            db.child(pidevicename+"_CONTROL").update({
                    'buzzer': str(0),
                    'led': str(0),
                    'lcdbkB': str(0),
                    'lcdbkG': str(0),
                    'lcdbkR': str(10),
                    'lcdscr': str(1),
                    'rlyfan': str(0),
                    'relay1': str(0)})
            
        
        
    except KeyboardInterrupt:
        digitalWrite(led, 0)
        break
    except TypeError:
        print("Type Error occurs")
        break
    except IOError:
        print("I/O error occurs.")
        break
    
    