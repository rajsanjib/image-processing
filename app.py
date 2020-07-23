from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import os
import json
# import image_segmentation
from main import main
from main.convert_pdf import convert
import sys
import argparse
import glob
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(filename='api.log', level=logging.DEBUG)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/extract_pan_card', methods=["POST"])
def extract_pan_card():
    content = request.data.decode('utf-8')
    data_dict = json.loads(content)
    im_b64 = data_dict['image']
    try:
        response = main.panToTxt(im_b64)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/extract_adhar_card', methods=["POST"])
def extract_adhar_card():
    content = request.data.decode('utf-8')
    data_dict = json.loads(content)
    im_b64 = data_dict['image']
    try:
        response = main.adharToTxt(im_b64)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/compare_faces', methods=["post"])
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

@app.route('/convert_pdf', methods=["POST"])
def convert_pdf():
    if request.method == 'POST':
        content = request.data.decode('utf-8')
        data_dict = json.loads(content)
        file = data_dict['file']
        if not file:
            return {"message": "pdf file not found!"}
        # if user does not select file, browser also
        # submit an empty part without filename
        try:
            response = convert(file)
        except Exception as e:
            response = f"[ERROR]: {e}"
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
