from PIL import Image
import os
import io

list  = []

for file in os.listdir():
    if file.endswith(".png"):
        image = open(file,"rb")
        list.append(image)

print((list[0]))

