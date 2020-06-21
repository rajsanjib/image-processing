from flask import Flask, render_template, request
import os
# import image_segmentation
from main import main
import sys
import argparse

app = Flask(__name__)

@app.route('/')
def index():
    # return (os.getcwd())
    return render_template("index.html")

@app.route("/upload-image", methods=["POST"])
def upload_image():
    if request.files:
        image = request.files["image"]
        image.save('images/'+image.filename)
    data= main.imgToTxt('images/'+image.filename)
    return data

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='8000', debug=True)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image to be OCR'd")
    args = vars(ap.parse_args())
    image = args["image"]
    data = main.imgToTxt(image)
    if(data['Output']):
        data = data['Output']
        print('\t', "|+++++++++++++++++++++++++++++++++++++++++++++|")
        print('\t', '|', 'Name:','\t', data['Name'])
        print('\t', "|---------------------------------------------|")
        print('\t', '|', 'Fathers Name:', '\t', data['Fathers Name'])
        print('\t', "|---------------------------------------------|")
        print('\t', '|', 'DOB:', '\t', data['DOB'])
        print('\t', "|---------------------------------------------|")
        print('\t', '|', 'PAN:', '\t', data['pan-id'])
        print('\t', "|---------------------------------------------|")
    else:
        print("No text found!")
