import cv2
import numpy as np
import random as rng
from matplotlib import pyplot as plt
from main import text_recognition

def preprocess():
    img = crop_card(img)

    #Apply Thresholding
    _, tH = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)

    return tH

def crop_out_template(img):
    tmp = cv2.imread('images/templates/logo.jpeg')

    # Resize template if template is bigger than the image
    if tmp.shape[1] > img.shape[1]:
        ratio = img.shape[1]/tmp.shape[1]
        tmp = cv2.resize(tmp, (0,0), fx=ratio, fy=ratio)
    c, w, h = tmp.shape[::-1]

    # Apply template Matching
    res = cv2.matchTemplate(img,tmp,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    ## Crop Image
    l = int(bottom_right[0]/2)
    y = bottom_right[1]
    img = img[y:,0:l]
    return img

def crop_card(image):
    # Find countour by color range
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([36,22,22])
    upper_blue = np.array([180,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange (hsv, lower_blue, upper_blue)
    bluecnts = cv2.findContours(mask.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(bluecnts)>0:
        blue_area = max(bluecnts, key=cv2.contourArea)
        (xg,yg,wg,hg) = cv2.boundingRect(blue_area)
        image = image[yg:yg+hg, xg:xg+wg]
    return image
