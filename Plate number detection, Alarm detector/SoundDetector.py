from time import *
from grovepi import *
from grove_rgb_lcd import *
from pyrebase import pyrebase
from random import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

pidevicename = "CR01"

pin_buz = 5
pin_snd = 14
pinMode(pin_buz,"OUTPUT")
pinMode(pin_snd, "INPUT")

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
    "storageBucket": "bait-2123-iot-g6.appspot.com"    
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

def starting():
    db.child(pidevicename+"_CONTROL").update({
            'buzzer': str(0),
            'lcdbkB': str(0),
            'lcdbkG': str(10),
            'lcdbkR': str(0),
            'lcdscr': str(1),
            'lcdtxt': str("Program running="),
            'relay1': str(1),
            'relay2': str(1)})

def updateSound(sound):
    s = str(sound)
    data = {"Sound":s}
    db.child(pidevicename+"_CONTROL").update(data)#

def updateDetectedAlarm():
    db.child(pidevicename+"_CONTROL").update({
            'buzzer': str(1),
            'lcdbkB': str(0),
            'lcdbkG': str(0),
            'lcdbkR': str(10),
            'lcdscr': str(1),
            'lcdtxt': str("=Alarm detected="),
            'rlyfan': str(0),
            'relay1': str(0),
            'relay2': str(0)})
    sleep(3)
    db.child(pidevicename+"_CONTROL").update({'buzzer': str(0)})
    
def updateNoDetectedAlarm():
    db.child(pidevicename+"_CONTROL").update({
            'buzzer': str(0),
            'lcdbkB': str(0),
            'lcdbkG': str(10),
            'lcdbkR': str(0),
            'lcdscr': str(1),
            'lcdtxt': str("No alarm detect="),
            'rlyfan': str(0),
            'relay1': str(1),
            'relay2': str(1)})

def sendMailSmartAlarmDetector(currentTime):
    sender_email = "iot2123g6@gmail.com"
    receiver_email = "cuimay1998@gmail.com"
    password = "2123B@iti0t"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Smart Parking System: Car Alarm Detected"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Alert: Car Alarm Detected
    Hi,
    Your car alarm is detected at the parking slot. 
    Please check if any incident has happened and triggered the car alarm."""
    html = """\
    <html>
      <body>
        <h2>Alert: Car Alarm Detected</h2>
        <p><br>Hi,<br><br>
           Your car alarm is detected at the parking slot at """ + currentDate + " " + currentTime + """.<br><br>
           Please check if any incident has happened and triggered the car alarm.<br><br>
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        server.quit()
        
starting() #update starting data in firebase
while True:
    try:
        sleep(3)
        currentDate = str(strftime("%Y-%m-%d", localtime()))
        currentTime = str(strftime('%H:%M:%S', localtime()))
        sound = analogRead(pin_snd)
        print("Sound = %d" %(sound))
        updateSound(sound) #update sound(input) in firebase
        
        if(sound > 500):
            updateDetectedAlarm() #update output data in school firebase
            print("At date " , currentDate , ", time " , currentTime)
            print("Car alarm detected")
            sendMailSmartAlarmDetector(currentTime)
            db2.child("Smart_Alarm").update({'Status':str(1)})
        else:
            updateNoDetectedAlarm() #update output data in school firebase
            print("At date " , currentDate , ", time " , currentTime)
            print("No car alarm detected")
            db2.child("Smart_Alarm").update({'Status':str(0)})
            
    except KeyboardInterrupt:
        setText("Progeam Exited")
        break
    except TypeError:
        print("Type Error occurs")
    except IOError:
        print("IO Error occurs")
