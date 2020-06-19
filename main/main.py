import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import sys
import re
import dateutil.parser as dparser
from main import image_segmentation
from main.helper import filter_text

def imgToTxt(imagePath = 'image/pan_card_11.jpg'):
    image = cv2.imread(imagePath)
    image = image_segmentation.crop_card(image)
    image = image_segmentation.crop_out_template(image)
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
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

    out = []
    output = image.copy()
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        if w > 15 and h > 15:
            text = pytesseract.image_to_string(roi, config=config)
            # if(text == ''):
            #     sorted_ctrs.pop(i)
            #     continue
            out.append(text)
            cv2.rectangle(output,(x,y),( x + w, y + h ),(0,255,0),2)
            cv2.putText(output, text, (x, y + 30),
    			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (25, 0, 51), 2)
    outpath = 'images/out/'+imagePath.replace('images/', '')
    cv2.imwrite(outpath, output)
    return({'Output': filter_text(out), 'path':outpath})
