from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import os
import json
# import image_segmentation
from main import main
import sys
import argparse
import glob
import logging


app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='api.log', level=logging.DEBUG)

@app.route('/extract-pan-card', methods=["POST"])
def extract_pan_card():
    content = request.data.decode('utf-8')
    data_dict = json.loads(content)
    im_b64 = data_dict['image']
    try:
        response = main.panToTxt(im_b64)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/extract-adhar-card', methods=["POST"])
def extract_adhar_card():
    content = request.data.decode('utf-8')
    data_dict = json.loads(content)
    im_b64 = data_dict['image']
    try:
        response = main.adharToTxt(im_b64)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/compare-faces', methods=["post"])
def compare_faces():
    content = request.data.decode('utf-8')
    data_dict = json.loads(content)
    image1 = data_dict['image1']
    image2 = data_dict['image2']
    try:
        response = main.compare_images(image1, image2)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
