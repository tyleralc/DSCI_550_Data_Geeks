from PIL import Image
import os
import pytesseract as tess


tess.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'


fox=r'data/fox'
directory = os.fsencode(fox)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    try:
        img=Image.open(filename)
        text=tess.image_to_string(img)
        print()
    except:
        print('too big')


#img= Image.open(r'data\aljazeera\03-01-22.png')
# img= Image.open('fox_3_12_1.png')
# img2= Image.open('row-2-column-1.png')
# text=tess.image_to_string(img)
# text2=tess.image_to_string(img2)
# print(text)
# print('________________________')
# print(text2)
