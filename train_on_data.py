"""
Trainer based on:
https://github.com/Mjrovai/OpenCV-Face-Recognition/blob/master/FacialRecognition/02_face_training.py 
"""

import cv2
import numpy as np
from PIL import Image
import os
import re

# Path to training image dataset
path = f'datasets{os.sep}private'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(f'haar_cascades{os.sep}haarcascade_frontalface_default.xml')

# function to get the images and label data
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert to grayscale --> check if redundant as images already seem to be grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(re.search(r'(?:face-)(\d+)(?:.*)', imagePath).group(1))  #NOTE: id.group(1) will return the full string matching
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids
print ("\n [+] Training on dataset faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
recognizer.write(f'trainer{os.sep}private{os.sep}trainer.yml') 
# Print the numer of faces trained and end program
print(f"\n [+] {len(ids)} faces trained. Exiting Program")