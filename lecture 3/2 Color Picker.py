from PIL import Image
import os
from PIL import Image
file=input()
x,y=map(int,input().split(', '))
path='data/'+file
img = Image.open(path)
print(img.getbands())
try:
    print(img.getpixel((x, y)))
except IndexError:
    print( 'Not exist.')