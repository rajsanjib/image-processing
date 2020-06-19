from flask import Flask, render_template, request
import os
# import image_segmentation
from main import main

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
