"""
Dataset generator based on:
https://github.com/thecodacus/Face-Recognition/blob/master/dataSetGenerator.py
"""

import cv2
import os

path = os.path.dirname(os.path.abspath(__file__))
cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier(path+f'{os.sep}haar_cascades{os.sep}haarcascade_frontalface_default.xml')
i=0
offset=50
register_message = """
                   Registering new face...
                   Please Enter A User ID: 
                   """
# print(register_message)
u_id = input(register_message)
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        i=i+1
        cv2.imwrite(f"datasets{os.sep}private{os.sep}face-"+u_id +'.'+ str(i) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.waitKey(100)
    if i>40:
        cam.release()
        cv2.destroyAllWindows()
        break