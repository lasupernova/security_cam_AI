## To DO: figure out how to get a not blurry image !!!! 
# re-use parts of the code from create_database ?

# import libraries
import cv2, time
from datetime import datetime
import pandas as pd
from Face_recognition import detect
import os
from send_alert import send_email
from PIL import Image as im
from helpers import pretty_print_timedelta, detect_blurry_img, get_contours
from threading import Timer

# create video capture object
video = cv2.VideoCapture(0, cv2.CAP_DSHOW) #pass already captured file (--> add path) or using webcam (0-n, depending on how many cameras are available in device)

# initiate necessary objects
first_frame = None 
status_list = []  # initiate list to record statuses
status_change_time =[]  # initiate list for status-change time
captured_images = []  # inititate list to save paths to captured images in

# initiate pandas dataframe
start = 0

while True:
    # check = reads first image in video --> used to check if video is running (returns True or False)
    # frame = reads initial within video capture objects (= a numpy arrays)
    check, frame = video.read()
    # print(frame)

    # initially set status to 0
    status = 0

    cnts = get_contours(first_frame, frame)

    # iterate over all saved contours and keep only contours with a size larger than a certain number of pixels

    if len(cnts) > 0:
        current_selection = {}
        def get_frame(first_frame=first_frame, current_selection=current_selection):
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            check, frame = video.read()
            cnts = get_contours(first_frame, frame)

            object_frame=[]
            for contour in cnts:
                if cv2.contourArea(contour) < 10000:
                    continue
                # if sufficiently large contour is captured, change status from 0 to 1
                status = 1
                # save coordinates of contours with size larger than defined above
                (x, y, width, height) = cv2.boundingRect(contour)
                # create rectagle object with coordinates specified in frame-object --> based on contours extracted from thresh_frame-object
                cv2.rectangle(frame,(x, y), (x+width, y+height), (0,255,43), 1)

                # get only part of frame capturing object
                obj = frame[y:y+height, x:x+width].copy()
                object_frame.append(obj)

            current_selection[now] = object_frame
            return current_selection

        t = Timer(0.1, get_frame)

    print(current_selection)

#     object_frame=[]
#     for contour in cnts:
#         if cv2.contourArea(contour) < 10000:
#             continue
#         # if sufficiently large contour is captured, change status from 0 to 1
#         status=1
#         # save coordinates of contours with size larger than defined above
#         (x, y, width, height) = cv2.boundingRect(contour)
#         # create rectagle object with coordinates specified in frame-object --> based on contours extracted from thresh_frame-object
#         cv2.rectangle(frame,(x, y), (x+width, y+height), (0,255,43), 1)

#         # get only part of frame capturing object
#         obj = frame[y:y+height, x:x+width].copy()
#         object_frame.append(obj)

#     # record status after this frame
#     status_list.append(status)

#     # save only last 2 items in list for improved memory usage
#     status_list = status_list[-2:]

#     # if current status is different from previous status, record the time
#     if len(status_list) > 1 and status_list[-1] != status_list[-2]:
#         current_time = datetime.now()
#         status_change_time.append(current_time)
#     if status_list[-1] == 1:  #if movement was detected --> add image for section
#         blur = detect_blurry_img(frame)
#         if blur == 0:
#             time_str = current_time.strftime("%Y%m%d_%Hh%Mm%Ss")
#             img_path = f'media{os.sep}motion{os.sep}{time_str}.jpg'
#             cv2.imwrite(img_path, frame)
#         else:
#             img_path = None

#     # show video in window
#     cv2.imshow("Capturing", frame)

#     # pass detected object frames to face_recognition.detect()
#     for obj in object_frame:
#         grey = cv2.cvtColor(obj, cv2.COLOR_BGR2GRAY)
#         # apply .detect() to frame and save output in canvas-variable
#         canvas = detect(grey, obj)
#         if len(canvas) > 0 and ((start==0) or (time.time() - start > 10)): 
#             #display canvas
#             cv2.imshow('Face detected', canvas)
#             cv2.imwrite(f'media{os.sep}ladron.jpg', canvas)
#             # image = cv2.imread(f'media{os.sep}test.jpg')  #cobvert array to image for send_email functions to work with
#             send_email(f'media{os.sep}ladron.jpg')
#             start = time.time()
#         elif len(canvas) > 0 and (time.time() - start < 30):
#             continue
#         else:
#             cv2.destroyWindow('Face detected')

#     # # show delta_frame -- uncomment for troubleshooting
#     # cv2.imshow("Difference", delta_frame)

#     # # show video with differences over the threshold -- uncomment for troubleshooting
#     # cv2.imshow("Threshhold", thresh_frame)

    # wait for input to close the window; if key is pressed on keyboard, the symbol of that key is stored in key (otherwise it will wait for the defined time)
    key = cv2.waitKey(10)

    # if a certain key is hit (here:q) --> break loop
    if key == ord('q'): #The ord() function returns an integer representing the Unicode character.
        # add entry if program is terminated while object is detected in the picture
        if status == 1:
            status_change_time.append(datetime.now())
        break

# # add status change values to df
# for i in range(0, len(status_change_time), 2):
#     duration = pretty_print_timedelta(status_change_time[i+1]-status_change_time[i])
#     image = f'media{os.sep}motion{os.sep}{status_change_time[i].strftime("%Y%m%d_%Hh%Mm%Ss")}.jpg' if img_path != None else None
#     df = df.append({"Start":status_change_time[i], "End":status_change_time[i+1], 
#                     "Duration":duration, 
#                     "Image": image},
#                     ignore_index=True)
# print(status_change_time[i+1]-status_change_time[i])
# print(type(status_change_time[i+1]-status_change_time[i]))
# # save df to .csv
# df.to_csv("security_cam.csv")

# release the camera
video.release()

# destroy all windows
cv2.destroyAllWindows()
