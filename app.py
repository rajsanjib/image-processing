from flask import Flask, render_template, request
import os
# import image_segmentation
from main import main
import sys
import argparse
import glob

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

def display(file, data):
    try:
        if(data):
            print('\t', "|+++++++++++++++++++++++++++++++++++++++++++++|")
            print('\t', '|', 'Image:','\t', file)
            print('\t', "|---------------------------------------------|")
            print('\t', '|', 'Name:','\t', data['Name'])
            print('\t', "|---------------------------------------------|")
            print('\t', '|', 'Fathers Name:  ', data['Fathers Name'])
            print('\t', "|---------------------------------------------|")
            print('\t', '|', 'DOB:', '\t', data['DOB'])
            print('\t', "|---------------------------------------------|")
            print('\t', '|', 'PAN:', '\t', data['pan-id'])
            print('\t', "|---------------------------------------------|")
            print('\n\n')
    except:
        print("Error:", data)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False,
                    help="path to input image to be OCR'd")
    ap.add_argument("-l", "--location", required=False,
                    help="path to directory containig input images to be OCR'd")
    args = vars(ap.parse_args())

    if(args['location']):
        files = []
        for ext in ("*.jpg","*.jpeg","*.png","*.webm"):
           files.extend(glob.glob(os.path.join(args['location'], ext)))
        for file in files:
            try:
                print(f'Working for {file}')
                data = main.imgToTxt(file)
                display(file, data)
            except Exception as e:
                data = f"[ERROR]: filename-{file} [{e}]"
                display(file, data)

    elif (args['image']):
        image = args["image"]
        data = main.imgToTxt(image)
        display(args['image'], data)
