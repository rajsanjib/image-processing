#### Text Detection on Image Using OpenCV and pytesseract

### 1. Clone the repo
``` git clone git@github.com:covideoin/image-processing.git ``` or
``` git clone https://github.com/covideoin/image-processing ```

### 2. Inside the image-processing directory

#### Create a virutalenv
``` virtualenv env -p python3 ```

#### Activate virutalenv

```source env/bin/activate```


### Install Dependencies
``` pip install -r requirements.txt ```

<i>**Might need to install following dependency for tensorflow</i>

```sudo apt-get install libcudart10.1```


### Setup Flask application with gunicorn and nginx
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

### Install dlib

Try installing python module of dlib ``` pip install dlib```
```
wget http://dlib.net/files/dlib-19.6.tar.bz2
tar xvf dlib-19.6.tar.bz2
cd dlib-19.6/
mkdir build
cd build
cmake ..
cmake --build . --config Release
sudo make install
sudo ldconfig
```


### apis
api is served on port 5000
- ##### /extract_pan_card
    - Request Method [POST]
    - Request

    ```{"image": "base64 encoded image"}```

    - Response
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

- ##### /extract_adhar_card
    - Method [POST]
    - Request

    ```{"image": "base64 encoded image"}```

    - Response
  ```
  data: {
    "DOB": "",
    "Name": "",
    "Gender": "",
    "adhar-id": ""
  },
  ```
  or
  ```
  data: {
      "address": address
  }
  ```
  if backside is given

- ##### /compare_faces
    - Method [POST]
    - Request
    ```
        {
         'image1': 'base64 encoded image',
         'image2': 'base64 encoded image'
        }
        ```

    - Response
      ```
        {
          score: match_value[0-1]
        }
      ```

- ##### /convert_pdf
    - Method [POST]
    - Request
    ```
        {
         'file': 'base64 encoded pdf file',
        }
        ```

    - Response
      ```
        {
          "image_filename": "filename.jpg"
        }
      ```
converted image will be stored as ```temp/pdf-to-image/filename.jpg```

- ##### /classify
  Returns predicted label of given document ==> pan-card | aadhar-card | driving-license
    - Method [POST]
    - Request
    ```
        {
         'image': 'base64 encoded image file',
        }
        ```

    - Response
      ```
        {
          "label": "pan-card/aadhar-card/driving-license"
        }
      ```
