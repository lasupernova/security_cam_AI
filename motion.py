# import libraries
import cv2, time
from datetime import datetime
import pandas as pd
from Face_recognition import detect

# create video capture object
video = cv2.VideoCapture(0,cv2.CAP_DSHOW) #pass already captured file (--> add path) or using webcam (0-n, depending on how many cameras are available in device)

# initiate necessary objects
first_frame = None 
status_list = [] # initiate list to record statuses
status_change_time =[] # initiate list for status-change time
df = pd.DataFrame(columns=['Start', 'End', 'Duration']) #initiate dataframe to record entry and exit times and duration

# initiate pandas dataframe

while True:
    # check = reads first image in video --> used to check if video is running (returns True or False)
    # frame = reads initial within video capture objects (= a numpy arrays)
    check, frame = video.read()
    # print(frame)

    # initially set status to 0
    status=0

    # convert first video frame to None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    # add gaussian blur in order to smooth the image and thus remove noise --> this improves accuracy in calculating the different between frames later on
    gray = cv2.GaussianBlur(gray, (15,15),0)

    # if nothing stored in first_frame yet, replace it with frame (--> if sth is stored already, it means, that is not the first image in the currrent video)
    if first_frame is None:
        first_frame = gray
        continue #skip rest of code in loop and go directly to next iteration

    # compare current frame to firs_frame and calculate difference between the two --> this returns an image (=diff-image)
    delta_frame = cv2.absdiff(first_frame, gray)


    #classify differences --> NOTE: white corresponds to 0 --> highest difference is shown in white; here: a difference of over 30 will only be considered
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1] #returns a tuple --> only second tuple-item (=the actual threshold-frame) is needed in this case

    # smooth thresh-frame in order to get rid of black spots
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=20)

    # find contours in thresh_frame and store all found contours in cnts-variable
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #--> returns a tuple

    # iterate over all saved contours and keep only contours with a size larger than a certain number of pixels
    object_frame=[]
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        # if sufficiently large contour is captured, change status from 0 to 1
        status=1
        # save coordinates of contours with size larger than defined above
        (x, y, width, height) = cv2.boundingRect(contour)
        # create rectagle object with coordinates specified in frame-object --> based on contours extracted from thresh_frame-object
        cv2.rectangle(frame,(x, y), (x+width, y+height), (0,255,43), 1)

        # get only part of frame capturing object
        obj = frame[y:y+height, x:x+width].copy()
        object_frame.append(obj)

    # record status after this frame
    status_list.append(status)

    # save only last 2 items in list for improved memory usage
    status_list = status_list[-2:]

    # if current status is different from previous status, record the time
    if len(status_list) >1 and status_list[-1] != status_list[-2]:
        status_change_time.append(datetime.now())

    # show video in window
    cv2.imshow("Capturing", frame)

    # pass detected object frames to face_recognition.detect()
    for obj in object_frame:
        grey = cv2.cvtColor(obj, cv2.COLOR_BGR2GRAY)
        # apply .detect() to frame and save output in canvas-variable
        canvas = detect(grey, obj)
        if len(canvas) > 0:
            #display canvas
            cv2.imshow('Face detected', canvas)
        else:
            cv2.destroyWindow('Face detected')

    # # show delta_frame
    # cv2.imshow("Difference", delta_frame)

    # # show video with differences over the threshold
    # cv2.imshow("Threshhold", thresh_frame)

    # wait for input to close the window; if key is pressed on keyboard, the symbol of that key is stqored in key (otherwise it will wait for the defined time)
    key=cv2.waitKey(10)

    # if a certain key is hit (here:q) --> break loop
    if key == ord('q'): #The ord() function returns an integer representing the Unicode character.
        # add entry if program is terminated while object is detected in the picture
        if status == 1:
            status_change_time.append(datetime.now())
        break

# add status change values to df
for i in range(0, len(status_change_time), 2):
    df = df.append({"Start":status_change_time[i], "End":status_change_time[i+1], "Duration":status_change_time[i+1]-status_change_time[i]},
                    ignore_index=True)

# save df to .csv
df.to_csv("security_cam.csv")

# release the camera
video.release()

# destroy all windows
cv2.destroyAllWindows()