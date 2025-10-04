from PIL import Image
from numpy.ma.extras import average


def greyscale(img,filter=None):
    new = Image.new("L", img.size)
    if filter is None:
        key=lambda x:x[0]
    if filter == 'Overexposed':
        key=lambda x:max(x)
    elif filter == 'Underexposed':
        key=lambda x:min(x)
    elif filter == 'Normal greyscale':
        key=lambda x:average(x)
    x, y = img.size
    for i in range(x):
        for j in range(y):
            new.putpixel((i, j), key(img.getpixel((i, j))))
    return new

file_name = input("File name: ")
if file_name == '':
    file_name = 'jellyfish.png'
filter_kind = 'Underexposed'#input("Filter: ")
origin = Image.open("data/" + file_name)
filtered = greyscale(origin, filter_kind)
filtered.show()
filtered.save("data/" + 'output.png')