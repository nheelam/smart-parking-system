from time import *
from grovepi import *
from pyrebase import pyrebase
from FakeDevices import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from grove_rgb_lcd import *

pidevicename = "CR01"

DHT = 0
htp = 4

pinMode(htp, "INPUT")
    
    
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


def sendMailSmartTemperature(temperature, humidity, currentTime):
    sender_email = "iot2123g6@gmail.com"
    receiver_email = "iot2123g6@gmail.com"
    password = "2123B@iti0t"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Smart Parking System: High Temperature Detected"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Warning: High Temperature Detected
    Hi,
    High Temperature detected at your parking slot. 
    Fire extinguisher activated to lower down the temperature
    Light and Alarm activated."""
    html = """\
    <html>
      <body>
        <h2>Warning: High Temperature Detected</h2>
        <p><br>Hi,<br><br>
           High Temperature detected at your parking slot at """ + currentTime + """.<br><br>
           Temperature Detected is """ + temperature + """ °C.<br><br>
           Humidity Detected is """ + humidity + """ %.<br><br>
           Fire extinguisher activated to lower down the temperature.<br><br>
           Light and Alarm activated.<br>
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



def writeDataHighTemp():
    data = {'buzzer': str(1),
        'camera': str(0),
        'lcdbkB': str(0),
        'lcdbkG': str(0),
        'lcdbkR': str(10),
        'lcdscr': str(1),
        'lcdtxt': str("===High Temp===="),
        'led': str(1),
        'ledlgt': str(0),
        'mqtten': str(1),
        'oledsc': str(0),
        'relay1': str(1),
        'relay2': str(1),
        'rlyfan': str(0),
        'sound' : str(234),
        'ult1': str(143)}
    
    db.child(pidevicename+"_CONTROL").update(data)
    
def writeDataModerateTemp():
    data = {'buzzer': str(0),
        'camera': str(0),
        'lcdbkB': str(0),
        'lcdbkG': str(10),
        'lcdbkR': str(10),
        'lcdscr': str(1),
        'lcdtxt': str("=Moderate Temp=="),
        'led': str(1),
        'ledlgt': str(0),
        'mqtten': str(1),
        'oledsc': str(0),
        'relay1': str(1),
        'relay2': str(0),
        'rlyfan': str(1),
        'sound' : str(234),
        'ult1': str(143)}
    
    db.child(pidevicename+"_CONTROL").update(data)
    
    
def writeDataNormalTemp():
    data = {'buzzer': str(0),
        'camera': str(0),
        'lcdbkB': str(0),
        'lcdbkG': str(10),
        'lcdbkR': str(0),
        'lcdscr': str(1),
        'lcdtxt': str("==Normal Temp==="),
        'led': str(1),
        'ledlgt': str(0),
        'mqtten': str(1),
        'oledsc': str(0),
        'relay1': str(0),
        'relay2': str(0),
        'rlyfan': str(0),
        'sound' : str(234),
        'ult1': str(143)}

    db.child(pidevicename+"_CONTROL").update(data)

def writeDataDefSetting():
    data = {'buzzer': str(0),
        'camera': str(0),
        'lcdbkB': str(0),
        'lcdbkG': str(10),
        'lcdbkR': str(0),
        'lcdscr': str(1),
        'lcdtxt': str("=App is running="),
        'led': str(0),
        'ledlgt': str(0),
        'mqtten': str(1),
        'oledsc': str(0),
        'relay1': str(0),
        'relay2': str(0),
        'rlyfan': str(0),
        'sound' : str(234),
        'ult1': str(143)}
    
    db.child(pidevicename+"_CONTROL").update(data)
    
while True:
    try:
        print("")
        sleep(1.0)
        [temp, hum] = dht(htp, DHT)
        
        t = str(temp)
        h = str(hum)
        
        data2 = {"temp":str(hum),
                "hum":str(temp)}
        db2.child("Smart_Temperature").update(data2)
        
        print('Temp: ', temp, '\u00b0c', '\tHum: ', hum, '%')
        
        if 50 < temp < 79:
            print("Detected that temperature is slighty higher.")
            currenttime = str(time.strftime('%H:%M:%S'))
            #setText('Temp: ', t, '\u00b0c', '\tHum: ', h, '%')
            print(currenttime)
            writeDataModerateTemp()
            
        elif temp >= 80:
            print("High temperature detected.")
            currenttime = str(time.strftime('%H:%M:%S'))
            sendMailSmartTemperature(t, h, currenttime)
            #setText('Temp: ', t, '\u00b0c', '\tHum: ', h, '%')
            print(currenttime)
            writeDataHighTemp()
            
        else:
            print("Normal Temperature")
            writeDataNormalTemp()
            #writeDataDefSetting()
            
    except KeyboardInterrupt:
        print('Program Exited')
        break
    except TypeError:
        print("Type Error occurs")
        break
    except IOError:
        print("I/O Error occurs")
        break
    
# default configuration
db.child(pidevicename+"_CONTROL").update({
                    'buzzer': str(0),
                    'camera': str(0),
                    'lcdbkB': str(0),
                    'lcdbkG': str(10),
                    'lcdbkR': str(0),
                    'lcdscr': str(1),
                    'lcdtxt': str("=App is running="),
                    'led': str(0),
                    'ledlgt': str(0),
                    'mqtten': str(1),
                    'oledsc': str(0),
                    'relay1': str(0),
                    'relay2': str(0),
                    'rlyfan': str(0),
                    'sound' : str(234),
                    'ult1': str(143)})