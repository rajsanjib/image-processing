import cv2
import numpy as np
import pytesseract

import sys
import re
import os
import base64
import json
from main import image_segmentation
from main.helper import filter_text

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

def imgToTxt(im_b64):
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    # image = crop_image(imagePath)
    # cv2.imshow("Cropped Image", image)
    # cv2.waitKey(0)
    image = image_segmentation.crop_card(image)
    image = image_segmentation.crop_out_template(image)

    # cv2.imshow("Cropped Image", image)
    # cv2.waitKey(0)
    #grayscale
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
                  # if signature is not None:
                  #   cv2.imwrite('images/signature/'+imagePath.replace('images/', ''), signature)
                  _, im_arr = cv2.imencode('.jpeg', signature)
                  im_bytes = im_arr.tobytes()
                  im_b64 = base64.b64encode(im_bytes)

            # data["signature"] = base64.b64encode(bytes(im_b64, 'utf-8')).decode("ascii")
            # data["signature"] = im_b64.decode['ascii']

            out.append(text)

    data['data'] = filter_text(out)
    return data
