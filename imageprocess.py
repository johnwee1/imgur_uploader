import os
from PIL import Image
import uploader
import warnings

# Turn off warning for decompression bombs. Only do this if you are certain the image source if safe
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

IMAGE_TARGET_SIZE = 5000000

def compress_img(filename):

    img = Image.open(filename)
    img_size = os.path.getsize(os.path.join(os.getcwd(), filename))
    if filename.startswith("CP_"):
        new_filename = filename
    else:
        new_filename = "CP_" + filename

    # Base case: image is smaller than limit
    if img_size < IMAGE_TARGET_SIZE:
        img.save(new_filename)
        return new_filename
    
    # Recursively compress the image
    quality = int(IMAGE_TARGET_SIZE/img_size * 100)
    img.save(new_filename, optimize = True, quality = quality)
    return compress_img(new_filename)



def getfile(client_id, album_hash):
    current_working_dir = os.getcwd()

    for filename in os.listdir(current_working_dir):
        if os.path.isfile(os.path.join(current_working_dir, filename)):
            if filename.startswith("CP_") == True:
                continue
            ext = os.path.splitext(filename)[1]  # get extension
            if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
                new_filename = compress_img(filename)  # Returns ref to new compressed file
                uploader.upload_image(new_filename, client_id, album_hash)
                os.remove(os.path.join(current_working_dir, new_filename))  # deletes the compressed photo






