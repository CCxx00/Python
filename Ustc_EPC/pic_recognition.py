import pytesseract
from PIL import Image

image = Image.open('./image/checkcode.bmp')
vcode = pytesseract.image_to_string(image)
print (vcode)
