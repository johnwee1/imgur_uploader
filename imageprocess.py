import os
from PIL import Image
import uploader
QUALITY = 50

def compress_img(filename, overwrite = False):
    img = Image.open(filename)
    if not overwrite:
        new_filename = "CP_" + filename
        img.save(new_filename, optimize = True, quality = QUALITY)
    else:
        img.save(filename, optimize = True, quality = QUALITY/3)  # Reduce compression aggression
        new_filename = filename
    img_size = os.path.getsize(os.path.join(os.getcwd(), new_filename))
    if img_size > 5000000:
        return compress_img(new_filename, True)  # Recursively compress until image is smaller than limit
    else:
        return new_filename



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






