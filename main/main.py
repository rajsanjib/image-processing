import cv2
import numpy as np
import pytesseract
from skimage.measure import compare_ssim
import imutils

import sys
import re
import os
import base64
import json

from main import image_segmentation
from main.utils.text_helper import *
from main.utils.utils import *

SIGNATURE_WIDTH = 350
SIGNATURE_HEIGHT = 70

config = ('-l eng --oem 1 --psm 3')


def get_signature(text, image, roi, x, y, w, h):
    try:
        if '\n' in text:
            signature = image[y + h - 100: y + h, x: x + SIGNATURE_WIDTH]
        elif text == 'Signature':
            signature = image[y - SIGNATURE_HEIGHT: y + 50, x:x + SIGNATURE_WIDTH]
    except:
        signature = None
    return signature

def panToTxt(im_b64):
    # image = b64_to_img(im_b64)
    image = cv2.imread(im_b64)

    image = image_segmentation.crop_card(image)
    image = image_segmentation.crop_out_template(image, template = 'images/templates/logo.jpeg')

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    #dilation
    kernel = np.ones((10,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    #find contours
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #sort contours
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[1])

    out = []
    data = {}
    output = image.copy()
    for i, ctr in enumerate(sorted_ctrs):
        # Get bounding box
        x, y, w, h = cv2.boundingRect(ctr)

        # Getting ROI
        roi = image[y:y+h, x:x+w]

        if w > 15 and h > 15:
            text = pytesseract.image_to_string(roi, config=config)

            sign = ['Signature', 'signature', 'sign']
            for s in sign:
                if s in text:
                  signature = get_signature(text, image, roi, x, y, w, h)
                  if signature is not None:
                    if not os.path.exists('images/signature'):
                        os.makedirs('images/signature')
                    cv2.imwrite('images/signature/'+im_b64.replace('images/', ''), signature)
                  # _, im_arr = cv2.imencode('.jpeg', signature)
                  # im_bytes = im_arr.tobytes()
                  # im_b64 = base64.b64encode(im_bytes)
                  # data["signature"] = im_b64.decode('ascii')
                  # final_data = json.dumps(data)
                  # final_data = json.loads(final_data)
            out.append(text)
    data["data"] = filter_text(out)
    return data

def adharToTxt(im_b64):
    print("Got")
    # image = b64_to_img(im_b64)
    image = cv2.imread(im_b64)

    # image = image_segmentation.crop_card(image)
    image = image_segmentation.crop_out_template(image, template = 'images/templates/adhar_card.jpg')
    #grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #binary
    ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    #dilation
    kernel = np.ones((10,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)

    config = ('-l eng --oem 1 --psm 6')
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
            if "Address" in text:
                return get_address(image)
            out.append(text)
            cv2.rectangle(output,(x,y),( x + w, y + h ),(0,255,0),2)
            cv2.putText(output, text, (x, y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (25, 0, 51), 2)

    return filter_text_for_adhar(out)

def get_address(image):
    c, w, h = image.shape[::-1]
    image = image[0:h, int(w/2.5):w]
    address = pytesseract.image_to_string(image, config=config)
    address = filter_address(address)
    return {'Address': address}

def compare_images(img_1, img_2):
    # load the two input images
    # imageA = b64_to_img(img_1)
    # imageB = b64_to_img(img_2)
    imageA = cv2.imread(img_1, 1)
    imageB = cv2.imread(img_2, 1)
    
    faceA = get_face(imageA)
    faceB = get_face(imageB)
    # convert the images to grayscale
    grayA = cv2.cvtColor(faceA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(faceB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    return {"score":score}
