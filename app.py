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
        response = main.imgToTxt(image)
    except Exception as e:
        response = f"[ERROR]: {e}"
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
