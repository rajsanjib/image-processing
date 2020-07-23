import cv2
import time
import numpy as np
import math
import glob, os

##################
DELAY = 0.02
USE_CAM = 1
IS_FOUND = 0

MORPH = 7
CANNY = 250
##################
# 420x600 oranı 105mmx150mm gerçek boyuttaki kağıt için
_width  = 600.0
_height = 420.0
_margin = 0.0
##################


def line_len(line):
	for x1, x2, y1, y2 in line:
		return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

def find_border(image):
	try:
		rgb = cv2.imread(image, 1)


		gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )

		gray = cv2.bilateralFilter( gray, 1, 10, 120 )

		# wide = cv2.Canny(gray, 10, 200)
		# tight = cv2.Canny(gray, 225, 250)
		# edges  = auto_canny(gray)

		edges = cv2.Canny(gray, 10, 200)

		kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )

		closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

		contours, h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

		# Finding contour with largest area
		c = max(contours, key = cv2.contourArea)

		width, height = rgb.shape[::2]
		(x,y,w,h) = cv2.boundingRect(c)
		if w > width*0.7 and h > height*0.6:
			# cv2.rectangle(rgb, (x,y), (x+w,y+h), (0,255,0), 2)
			rgb = rgb[y: y+h, x:x+w]
			return rgb
	except:
		return image
