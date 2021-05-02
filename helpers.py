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



if __name__ == "__main__":
    detect_blurry_img()

    