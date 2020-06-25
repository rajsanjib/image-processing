#### Text Detection on Image Using OpenCV and pytesseract

### 1, Clone the repo
``` git clone git@github.com:covideoin/image-processing.git ``` or
``` git clone https://github.com/covideoin/image-processing ```

### 2. Inside the image-processing directory

#### Create a virutalenv
``` virtualenv env -p python3 ```

#### Activate virutalenv

```source env/bin/activate```


### Install Dependencies
``` pip install -r requirements.txt ```

### Setup Flask application with gunicorn and nginx
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04


### apis
#### Request
- /extract-pan-card
    - Method [POST]
    - Send [image] in base64 format

#### Response
```
{
  data: {
    "DOB": "",
    "Fathers Name": "",
    "Name": "",
    "pan-id": ""
  },
  signature: "base64 data"
}
```
