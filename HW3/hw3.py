from PIL import Image
import os
import pytesseract as tess

tess.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
<<<<<<< HEAD
#img= Image.open(r'data\aljazeera\03-01-22.png')
img= Image.open('fox_3_12_2.png')
#img2= Image.open('row-1-column-1.png')
text=tess.image_to_string(img)
#text2=tess.image_to_string(img2)
print(text)
print('________________________')
#print(text2)
=======


# fox=r'data/fox'
# directory = os.fsencode(fox)
    
# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     try:
#         img=Image.open(filename)
#         text=tess.image_to_string(img)
#         print(text)
#     except:
#         print('too big')


img= Image.open(r'data\fox\03-12-22-20.png')
#img= Image.open('95-Most-Important-Words-List-in-English.png')
# img2= Image.open('row-2-column-1.png')
text=tess.image_to_string(img)
# text2=tess.image_to_string(img2)
print(text)
# print('________________________')
# print(text2)
>>>>>>> 7e1a96687d148108de3033773638056d03279a02
