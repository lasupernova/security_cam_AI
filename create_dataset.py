"""
Dataset generator based on:
https://github.com/thecodacus/Face-Recognition/blob/master/dataSetGenerator.py
"""

from PIL.Image import new
import cv2
import os, sys 
import re
from private_id_dict import id_dict  #added parent folder to __init__.py for (relative) import to work

path = os.path.dirname(os.path.abspath(__file__))
cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier(path+f'{os.sep}haar_cascades{os.sep}haarcascade_frontalface_default.xml')
offset=50
font = cv2.FONT_HERSHEY_SIMPLEX
register_message = """
                   Registering new face...
                   Please Enter A User ID: 
                   """

register_message = """
                   New or returning user?
                   Type 'n' for new or 'r' for returning: 
                   """
path = f'datasets{os.sep}private'
imagePaths = [os.path.join(path,f) for f in os.listdir(path)]  

def register_user(imagePaths=imagePaths): 
    existing_ids = set([int(re.search('(?:face-)(\d+)(?:.*)', img_path).group(1)) for img_path in imagePaths])  #use regex to extract all IDs
    max_id = max(existing_ids)  #get largest existing ID to infer new ID from it in next step
    current_id = max_id+1
    print(f"[+]\tHi new user!\nYou will have user ID {current_id}!")
    return current_id, 0

def get_returning_user_ID(imagePaths=imagePaths):
    current_id = None
    while current_id == None:
        user_name = input("Enter your name: ")
        try:
            current_id = [k for k,v in id_dict.items() if v == user_name][0]
        except:
            status = input("Sorry, no user with that name was found!\nDo you want to try entering your name again[y/n]?")
            if status == 'y':
                continue
            elif status == 'n':
                status = input("Do you want to register as a new user or exit? Type 'n' for new user or hit any other key for exit: ")
                if status != 'n':
                    sys.exit("\n[+]\tProgram closed.\n")
                else:
                    return register_user()
    # image_nums = [int(re.search(regex, img_path).group(0)) for img_path in imagePaths]   ##figure out why this regex is not working 
    image_nums_for_id = [int(img_path.split(".")[1]) for img_path in imagePaths if f"face-{current_id}." in img_path]  
    image_num = max(image_nums_for_id)
    print(f"[+]\tWelcome back {user_name}! Your ID is: {current_id} and you currently have {image_num} pictures.")
    return current_id, image_num

# print(register_message)
status = None
while status!='r' and status != 'n':
    status = input(register_message)

if status == 'n':
    current_id, num = register_user()
elif status == 'r':
    current_id, num = get_returning_user_ID()
else:
    print("ERROR! Invalid Input!")

print("\n[+]\tSMILE (or not)! Taking 40 more pictures to for your dataset.\n")
i = num
total = i + 40
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x,y,w,h) in faces:
        i+=1
        print(f"Picture number: {i}")
        cv2.imwrite(f"datasets{os.sep}private{os.sep}face-{current_id}.{i}.jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        cv2.imshow("Capturing...",im[y-offset:y+h+offset,x-offset:x+w+offset])
        cv2.waitKey(100)
    if i > total:
        cam.release()
        cv2.destroyAllWindows()
        break