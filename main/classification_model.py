from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import random
import cv2
import base64

MODEL_PATH = 'model/classifier.pt'
LABELS = ['pan-card', 'aadhar-card', 'driving-license']

def classify_image(im_b64):
    model = load_model(MODEL_PATH)

    im_bytes = base64.b64decode(im_b64)
    im_arr = np.fromstring(im_bytes, np.uint8)
    orig = cv2.imdecode(im_arr, cv2.IMREAD_COLOR)

    # pre-process our image by converting it from BGR to RGB channel
    # ordering (since our Keras mdoel was trained on RGB ordering),
    # resize it to 64x64 pixels, and then scale the pixel intensities
    # to the range [0, 1]
    image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (150, 150))
    image = image.astype("float") / 255.0

    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    # make predictions on the input image
    pred = model.predict(image)
    pred_labels = np.argmax(pred, axis = 1)
    return {"label": LABELS[pred_labels[0]]}
