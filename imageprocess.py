import os
from PIL import Image
import warnings

# Turn off warning for decompression bombs. Only do this if you are certain the image source if safe
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

IMAGE_TARGET_SIZE = 5000000

def compress_img(filepath):

    img = Image.open(filepath)
    img_size = os.path.getsize(filepath)
    img_name = os.path.basename(filepath)

    # Overwrites image if and only if the image is a duplicate (not the base image)
    if img_name.startswith("CP_"):
        dest_path = os.path.join(os.getcwd(), img_name)
    else:
        dest_path = os.path.join(os.getcwd(), "CP_" + img_name)

    # Base case: image is smaller than limit
    if img_size < IMAGE_TARGET_SIZE:
        img.save(dest_path)
        return dest_path
    
    # Recursively compress the image
    quality = int(IMAGE_TARGET_SIZE/img_size * 100)
    img.save(dest_path, optimize = True, quality = quality)
    return compress_img(dest_path)


def getfiles():

    files = []
    accepted_types = ['.jpg', '.jpeg', '.png']
    current_working_dir = os.getcwd()

    for file in os.listdir(current_working_dir):
        if os.path.isfile(os.path.join(current_working_dir, file)):
            if file.startswith("CP_") == True:
                continue
            # filter extension
            ext = os.path.splitext(file)[1].lower()  
            if ext in accepted_types:
                files.append(os.path.abspath(file))

    return files