# Face Recognition 
import cv2
import os

# load the required XML classifiers 
# --> these classifiers store the "templates" for recognizing models
face_cascade = cv2.CascadeClassifier(os.path.join('haar_cascades', 'haarcascade_frontalface_default.xml')) 
eye_cascade = cv2.CascadeClassifier(os.path.join('haar_cascades', 'haarcascade_eye.xml')) 
# print(os.path.join('haar_cascades', 'haar_cascade haarcascade_frontalface_default.xml'))
## function that uses cascades to detect a face
def detect(grey, frame):
    # NOTE: "If faces are found, it returns the positions of detected faces as Rect(x,y,w,h)" --> returns a tuple with 4 values
    faces = face_cascade.detectMultiScale(grey, 
                                          scaleFactor=1.3,  #"Parameter specifying how much the image size is reduced at each image scale"
                                          minNeighbors=8 # "Parameter specifying how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces: higher value results in less detections but with higher quality"
                                          )
    # draw rectangle around found face coordinates
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, #image to draw the rectangle in
                      (x,y), #x and y coordinates
                      (x+w, y+h), # width and heigth added to x and y
                      (0,0,255), #rectangle color
                      2 #rectangle line width
                      )
        #detect eyes within rectangles
        roi_grey = grey[y:y+h, x:x+w] #use only space within rectangle in order to save time and computing power
        roi_clr = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_grey, 
                                          scaleFactor=1.1,  #"Parameter specifying how much the image size is reduced at each image scale"
                                          minNeighbors=10 # "Parameter specifying how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces: higher value results in less detections but with higher quality"
                                          )
        # plot separate rectangles around the eyes
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_clr, (ex,ey), (ex+ew, ey+eh), (0,255,0), 1)

    if len(faces) > 0:  #rturn frame only if at least 1 face was detected
        print(f"FACES: ", faces)
        return frame #includes drawn rectangles (also of roi_clr as that is a part of frame)
    else:
        return []


if __name__ == '__main__':
    ## detect faces in webcam video
    video_capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW) #start video on webcam

    while True:
        # get last frame of the video (--> .read() returns a tupl with two values and the second of those values is the last frame)
        _, frame = video_capture.read()
        # make frame grey
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # apply .detect() to frame and save output in canvas-variable
        canvas = detect(grey, frame)
        #display canvas
        cv2.imshow('Video', canvas)
        #break loop when 'q' is pressed on keyboard
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # turn off webcam
    video_capture.release()

    # close all windows
    cv2.destroyAllWindows()
    
