from flask import Flask, render_template, request, jsonify
import os
# import image_segmentation
from main import main
import sys
import argparse
import glob
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract-pan-card', methods=["POST"])
def extract_pan_card():
    image = request.files['image']
    # try:
    image.save('images/'+image.filename)
    response = main.panToTxt('images/'+image.filename)
    # except Exception as e:
    #     response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/extract-adhar-card', methods=["POST"])
def extract_adhar_card():
    image = request.files['image']
    try:
        image.save('images/'+image.filename)
        response = main.adharToTxt('images/'+image.filename)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/compare-faces', methods=["post"])
def compare_faces():
    image1 = request.files['image1']
    image2 = request.files['image2']
    # try:
    image1.save('images/'+image1.filename)
    image2.save('images/2'+image2.filename)
    try:
        response = main.compare_images(('images/'+image1.filename), ('images/2'+image2.filename))
    except:
        response = {'message': 'Face does not match'}
    # except Exception as e:
    #     response = f'[ERROR]: {e}'
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
