import cv2
import numpy as np
import imutils
import easyocr
from time import *
from pyrebase import pyrebase

pidevicename = "CR01"

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
storage2 = firebase2.storage()

# school database
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("bait2123.iot.01@gmail.com","BeyondEducation")
db = firebase.database()

storage2.child("image/test.jpeg").download("","test_download.jpg")

currentDate = strftime("%d/%m/%Y", localtime())
currentTime = strftime("%H:%M:%S", localtime())
currentDateTime = currentDate + "  " + currentTime

img = cv2.imread('test_download.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 30, 200) #Edge detection

keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0,255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)

(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]

reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)

text = result[0][-2]
font = cv2.FONT_HERSHEY_SIMPLEX
res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)

print("The car plate number " + text +" is blocking others.\n")

acc = db2.child("user_registered").get()

for value in acc.each():
    acckey = value.key()
    platenum = db2.child("user_registered/"+acckey+"/plate_Number").get().val()
    
    if platenum == text:
        contactnum = db2.child("user_registered/"+acckey+"/contact_Number").get().val()
        warnName = db2.child("user_registered/"+acckey+"/name").get().val()
        print("Contact found: " + contactnum)
        print("Driver name: " + warnName)
        db2.child("Smart_Alarm").push({
            'Name': warnName,
            'Plate Number': text,
            'Contact Number': contactnum,
            'Date Time': currentDateTime})
        
        db.child(pidevicename+"_CONTROL").update({
            'relay1':str(1),
            'lcdbkB': str(0),
            'lcdbkG': str(0),
            'lcdbkR': str(35),
            'lcdtxt': str("DetectCarBlockin")})
        sleep(5)
        db.child(pidevicename+"_CONTROL").update({
            'lcdtxt': str("HPNO:"+contactnum+"=")})
