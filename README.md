#### Text Detection on Image Using OpenCV and pytesseract

### Create a virutalenv
``` virtualenv env -p python3 ```

#### Activate virutalenv

Linux ```source env/bin/activate```

Windows ```.\venv\Scripts\activate```


### Install Dependencies
``` pip install -r requirements.txt ```

### Run app
In root folder ``` python3 app.py```. Then open http://localhost:8000/ in browser

###Output Format
```
{
  data: {
    "DOB": "10/12/1983",
    "Fathers Name": "AMAR SINGH",
    "Name": "CHHOTU RAM",
    "pan-id": "BLUPS4233F"
  },
  "path": "images/out/pan_card_13.jpeg"
}
```
Yet to separate name, dob etc... Will be pushed on next commit

### Techniques used
1. crop image, take only the left half portion
2. Apply grayscaling, binary threshold and dilation.
3. Run pytesseract image to text on the result.
4. Returns all possible text fields.

### pytesseract config
1. language - English (en)
2. oem - 1 (Neural nets LSTM only)
3. psm - 7 (Treat the image as a single text line)
