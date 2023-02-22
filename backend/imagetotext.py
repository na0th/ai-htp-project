import base64
import sys

with open("backend\example.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print(str)
    # print(sys.getsizeof(str))

imgdata = base64.b64decode(str)
filename = 'example.jpg'  # I assume you have a way of picking unique filenames
with open(filename, 'wb') as f:
    f.write(imgdata)