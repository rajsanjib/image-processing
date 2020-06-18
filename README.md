### Text Detection on Image Using OpenCV and pytesseract
### Install Dependencies
- imutils
- numpy
- pytesseract
- cv2
- jupyter notebook

### Run
```Open image_segmentation.ipynb and give filename for image. Then run the notebook file```

### Techniques used
1. crop image, take only the left half portion
2. Apply grayscaling, binary threshold and dilation.
3. Run pytesseract image to text on the result.
4. Returns all possible text fields.

### pytesseract config
1. language - English (en)
2. oem - 1 (Neural nets LSTM only)
3. psm - 7 (Treat the image as a single text line)
