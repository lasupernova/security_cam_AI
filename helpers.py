import datetime
import cv2

def pretty_print_timedelta(delta):
    """
    Converts datetime.timedelta - object to string and returns a pretty printed version in the following format:
    "hh:mm:ss" or "more than 24 hours" in case the tiemdelta is over 24 hours.

    Parameters:
        delta (datetime.timedelta) - timedelta to be converted

    Returns:
        duration (str)
    """
    days = delta.days
    hh, remainder = divmod(delta.seconds, 3600)
    mm, ss = divmod(remainder, 60)

    if days == 0:
        return f"{hh}h:{mm}m:{ss}s"
    else:
        return "More than 24 hours!"


def detect_blurry_img(image=None):
    """
    Detects blurry images by computing the Laplacian of the image and returning the focus
	measure. This measure is the variance of the Laplacian (using cv2.Laplacian())

    Parameters:
        image (numpy.array) - image in array-form

    Returns:
        bool - 1 (blurry) or 0 (not blurry)
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #load image from array and convert image to grayscale 

    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var() 

    if laplacian < 250:  # image will be considered blurry for a Laplacian < 250
        return 1  #image is blurry
    else:  
        return 0  #not blurry 

def get_contours(first_frame, frame):
    """
    Extract contours from frame (=np.array representing an image) and return list of contour objects.

    Parameters:
        frame (numpy.array) - image in array-form

    Returns:
        cnts (list) - list of contour objects
    """

    # convert first video frame to None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    # add gaussian blur in order to smooth the image and thus remove noise --> this improves accuracy in calculating the different between frames later on
    gray = cv2.GaussianBlur(gray, (15,15),0)

    # if nothing stored in first_frame yet, replace it with frame (--> if sth is stored already, it means, that is not the first image in the currrent video)
    if first_frame is None:
        first_frame = gray
        return first_frame #skip rest of code in loop and go directly to next iteration

    # compare current frame to firs_frame and calculate difference between the two --> this returns an image (=diff-image)
    delta_frame = cv2.absdiff(first_frame, gray)

    #classify differences --> NOTE: white corresponds to 0 --> highest difference is shown in white; here: a difference of over 30 will only be considered
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1] #returns a tuple --> only second tuple-item (=the actual threshold-frame) is needed in this case

    # smooth thresh-frame in order to get rid of black spots
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=20)

    # find contours in thresh_frame and store all found contours in cnts-variable
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #--> returns a tuple

    return cnts


if __name__ == "__main__":
    detect_blurry_img()

    