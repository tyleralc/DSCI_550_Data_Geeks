from PIL import Image

import pytesseract as tess
tess.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#img= Image.open(r'data\aljazeera\03-01-22.png')
img= Image.open('95-Most-Important-Words-List-in-English.png')
text=tess.image_to_string(img)
print(text)

