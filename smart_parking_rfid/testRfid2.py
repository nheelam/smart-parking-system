from time import *
from grovepi import *
from pyrebase import pyrebase
from FakeDevices import *
import logging
from grove_rgb_lcd import *
from mfrc522 import SimpleMFRC522
writer = SimpleMFRC522()
import random

pidevicename = "CR01"
#cui may's firebase
# config = {
#     "apiKey": "AIzaSyB4TjvGmKN_9qjbFK4C0IGcl7c7F2FPmb0",
#     "authDomain": "bait2123-iot-77da8.firebaseapp.com",
#     "databaseURL": "https://bait2123-iot-77da8-default-rtdb.firebaseio.com/",
#     "storageBucket": "bait2123-iot-77da8.appspot.com"
# }
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# user = auth.sign_in_with_email_and_password("cuimay1998@gmail.com", "lcm2000590")
# db = firebase.database()

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

# group database
firebase2 = pyrebase.initialize_app(config2)
auth2 = firebase2.auth()
user2 = auth2.sign_in_with_email_and_password("iot2123g6@gmail.com","2123B@iti0t")
db2 = firebase2.database()

# school database
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("bait2123.iot.01@gmail.com","BeyondEducation")
db = firebase.database()


name = input('Please enter your name: ')
numberPlate = input('Please enter your car number plate: ')
contactnum = input('Please enter your contact number: ')
    
acc = db2.child("user_registered").get()
for value in acc.each():
    acckey = value.key()
    platenum = db2.child("user_registered/"+acckey+"/plate_Number").get().val()
    if numberPlate == platenum:
        print('Account already exists.')
        break
    else:
        number1 = random.randint(100,999)
        number2 = random.randint(1,3)
        textInt = int(str(number1) + str(number2))
        sector = textInt %10
        text = str(textInt)
        print('Your generated 4 digit pin number: ', text)
        print('Please tap the card on RFID reader/writer')
        writer.write_sector(text,sector)
        print('Successfully Registered Account.')
    
        db2.child("user_registered").push({
            'name': name,
            'plate_Number': numberPlate,
            'contact_Number': contactnum,
            'pin': text})
        break
                
            
            
    


#this part comment first so that it will not affect CR, during demo only uncomment it
"""    db.child(pidevicename+"_CONTROL").update({
            'relay1':str(0),
            'lcdbkB': str(0),
            'lcdbkG': str(35),
            'lcdbkR': str(0),
            'lcdtxt': str("=A RFID created=")})"""

#below are previous coding
"""    db.child(pidevicename+"_CONTROL_REGISTER").push({
        'Name': name,
        'Plate Number': numberPlate,
        'Contact Number': contactnum,
        'Rfid': text})"""
    
"""    db2.child(pidevicename+"_CONTROL_REGISTER").push({
        'Name': name,
        'Plate Number': numberPlate,
        'Contact Number': contactnum,
        'Rfid': text})"""
    
    

           
