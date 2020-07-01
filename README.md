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
api is served on port 5000
- ##### /extract-pan-card
    - Request Method [POST]
    - ```{"image": "base64 encoded image"}```

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

- ##### /extract-adhar-card
    - Method [POST]
    - ```{"image": "base64 encoded image"}```

    Response
```
  data: {
    "DOB": "",
    "Name": "",
    "Gender": "",
    "adhar-id": ""
  },

  or
  data: {
    address: address
  }
  if backside is given
```

- ##### /compare-faces
    - Method [POST]
    - ```
        {
         'image1': 'base64 encoded image',
         'image2': 'base64 encoded image'
        }
        ```

      Response
      ```
        {
          score: match_value[0-1]
        }
      ```
