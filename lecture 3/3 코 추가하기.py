
from PIL import Image
files=['data/smile.png',
       'data/smile_bw.png',
       'data/smile_rgb.png',
       'data/smile_rgba.png',
       'data/sad.png']
coords=[(18, 22),
       (18, 23),
       (19, 22),
       (19, 23),
       (20, 19),
       (20, 20),
       (20, 21),
       (20, 22),
       (20, 23),
       (21, 19),
       (21, 20),
       (21, 21),
       (21, 22),
       (21, 23)]
for path in files:
    img = Image.open(path)
    for coord in coords:
        img.putpixel(coord,0)
    img.save(path[:-4]+'_nose'+path[-4:])