import os
from PIL import Image

files = []
counter = 0
for file in os.listdir():
    # image = open(file)
    # files.append(file)

    if file != "rotate.py":
        print(file)
        image = Image.open(file)
        image.save(f"{counter}.png")
        counter += 1
