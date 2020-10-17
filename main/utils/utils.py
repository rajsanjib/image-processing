import base64
from base64 import b64decode
import cv2
import numpy as np
import uuid
import codecs

def b64_to_img(im_b64):
    im_bytes = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_GRAYSCALE)
    return image

def b64_to_pdf(pdf_b64):
    # Decode the Base64 string, making sure that it contains only valid characters
    bytes = b64decode(pdf_b64, validate=True)

    # Perform a basic validation to make sure that the result is a valid PDF file
    # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
    # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
    if bytes[0:4] != b'%PDF':
      raise ValueError('Missing the PDF file signature')

    filename = str(uuid.uuid4().fields[-1])[:5]
    path = 'temp/pdf/%s.pdf' % filename
    # Write the PDF contents to a local file
    with open(path, "wb") as f:
        f.write(bytes)

    return filename

def get_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        return roi_color
