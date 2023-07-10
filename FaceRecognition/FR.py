import numpy as np
import face_recognition as fr
import cv2
from pyrebase import pyrebase

# config = {
#     
#     # school device 01
#     "apiKey": "AIzaSyA-b-Fs1FWOjeN9qKuwKUZlIfUg_-6nPc0",
#     "authDomain": "bait2123-202109-01-default-rtdb.asia-southeast1.firebasedatabase.app",
#     "databaseURL": "https://bait2123-202109-01-default-rtdb.asia-southeast1.firebasedatabase.app/",
#     "storageBucket": "bait2123-202109-01.appspot.com" 
#     
# }
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

# # school database
# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# user = auth.sign_in_with_email_and_password("bait2123.iot.01@gmail.com","BeyondEducation")
# db = firebase.database()

video_capture = cv2.VideoCapture(0) #take the video from our webcam

niimin_image = fr.load_image_file("Niimin.jpg") #load the image

#take our image and analyze it so we can have the encoding of our face
#like distance between the eyes, the nose etc
#[0] there might be a lot of faces in the picture, but for this only one
niimin_face_encoding = fr.face_encodings(niimin_image)[0]

#if we want to add more faces, just [niimin_face_encoding, ..., ...]
known_face_encondings = [niimin_face_encoding]
known_face_names = ["Nii Min"]
name = "Unknown"

while True: 
    ret, frame = video_capture.read()
    
    #change the colour of the frame to rgb frame
    rgb_frame = frame[:, :, ::-1]
    
    #check whr r the faces in the frame
    face_locations = fr.face_locations(rgb_frame)
    
    face_encodings = fr.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = fr.compare_faces(known_face_encondings, face_encoding, tolerance = 0.6)

#         name = "Unknown"

        face_distances = fr.face_distance(known_face_encondings, face_encoding)

        best_match_index = np.argmin(face_distances)
        print (face_distances)
        
        if matches[best_match_index] and face_distances < 0.45:
            name = known_face_names[best_match_index]
        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Webcam_facerecognition', frame)
            

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    data2 = {
            'User': str(name)}
        
    db2.child('Smart_Light').update(data2)
    
#     db.child(pidevicename+"_CONTROL").update({
#                     'buzzer': str(0),
#                     'led': str(0),
#                     'lcdbkB': str(0),
#                     'lcdbkG': str(0),
#                     'lcdbkR': str(5),
#                     'lcdscr': str(1),
#                     'rlyfan': str(0),
#                     'relay1': str(1),
#                     'lcdtxt':str("   Assignment   ")})

video_capture.release()
cv2.destroyAllWindows()

