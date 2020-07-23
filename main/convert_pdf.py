from PIL import Image as Img
from wand.image import Image
import uuid
import numpy as np
import glob
import os
import sys
from main.utils.utils import b64_to_pdf

def convert(b64):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    if not os.path.exists('temp/pdf'):
        os.makedirs('temp/pdf')
    if not os.path.exists('temp/pdf-to-image'):
        os.makedirs('temp/pdf-to-image')
    pdf = b64_to_pdf(b64)
    #used to generate temp file name. so we will not duplicate or replace anything
    # try:
        #now lets convert the PDF to Image
        #this is good resolution As far as I know
    with Image(filename="temp/pdf/%s.pdf"%pdf, resolution=200) as img:
        #keep good quality
        img.compression_quality = 100
        #save it to tmp name
        img.save(filename="temp/pdf-to-image/%s.jpg" % pdf)
        return {"image_filename": "%s.jpg"%pdf}
    # except Exception as err:
    #     #always keep track the error until the code has been clean
    #     print (err)
    #     return False
    # else:
    #     """
    #     We finally success to convert pdf to image.
    #     but image is not join by it self when we convert pdf files to image.
    #     now we need to merge all file
    #     """
        # pathsave = []
        # try:
        #     #search all image in temp path. file name ends with uuid_set value
        #     list_im = glob.glob("temp/pdf-to-img/%s*.jpg" % pdf)
        #     list_im.sort() #sort the file before joining it
        #     imgs = [Img.open(i) for i in list_im]
        #     #now lets Combine several images vertically with Python
        #     min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
        #     imgs_comb = np.vstack(
        #         (np.asarray(i.resize(min_shape)) for i in imgs))
        #     # for horizontally  change the vstack to hstack
        #     imgs_comb = Img.fromarray(imgs_comb)
        #     pathsave = "temp/pdf-to-img/%s.jpg" % pdf
        #     #now save the image
        #     imgs_comb.save(pathsave)
        #     #and then remove all temp image
        #     for i in list_im:
        #         os.remove(i)
        # except Exception as err:
        #     print (err)
        #     return False

# if __name__ == "__main__":
#      arg = sys.argv[1]
#      result = convert(arg)
#      if result:
#         print( "[*] Succces convert %s and save it to %s" % (arg, result))
#      else:
#         print( "[!] Whoops. something wrong dude. enable err var to track it")
