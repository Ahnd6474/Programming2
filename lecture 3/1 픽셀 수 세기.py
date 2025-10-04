from PIL import Image
file=input()
path='data/'+file
img = Image.open(path)
print( img.width* img.height)

