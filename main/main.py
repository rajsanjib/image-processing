import cv2
import numpy as np
import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter
import sys
import re
import os
# import dateutil.parser as dparser
from main import image_segmentation
from main.helper import filter_text
from main.crop import crop_image

def imgToTxt(imagePath):
    # image = cv2.imread(imagePath)
    image = crop_image(imagePath)
    # cv2.imshow("Cropped Image", image)
    # cv2.waitKey(0)
    # image = image_segmentation.crop_card(image)
    # image = image_segmentation.crop_out_template(image)

    # cv2.imshow("Cropped Image", image)
    # cv2.waitKey(0)
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    #dilation
    kernel = np.ones((10,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    config = ('-l eng --oem 1 --psm 3')
    # Initializing data variable


    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])

    out = []
    output = image.copy()
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        if w > 15 and h > 15:
            text = pytesseract.image_to_string(roi, config=config)
            out.append(text)
            cv2.rectangle(output,(x,y),( x + w, y + h ),(0,255,0),2)
            cv2.putText(output, text, (x, y + 30),
    			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (25, 0, 51), 2)

    if not os.path.exists('images/out'):
        os.makedirs('images/out')
    # Get the name of image
    outpath = 'images/out/'+imagePath.replace('images/', '')
    # print("Collected: ", out)
    cv2.imwrite(outpath, output)
    # return({'Output': filter_text(out), 'path':outpath})
    return filter_text(out)
