from flask import Flask, render_template, request, jsonify
import os
# import image_segmentation
from main import main
import sys
import argparse
import glob

app = Flask(__name__)

@app.route('/extract-pan-card', methods=["POST"])
def extract_pan_card():
    image = request.json['image']
    try:
        response = main.panToTxt(image)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)

@app.route('/extract-adhar-card', methods=["POST"])
def extract_adhar_card():
    im_64 = request.json['image']
    response = main.adharToTxt(im_64)
    return jsonify(response)

@app.route('/compare-faces', methods=["post"])
def compare_faces():
    image1 = request.json['image1']
    image2 = request.json['image2']
    response = main.compare_images(image1, image2)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
