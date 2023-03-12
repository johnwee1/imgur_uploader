import os
import imageprocess
import uploader
APP_VERSION = "1.0"
DEFAULT_CLIENT_ID = "ae33cb66617c656" # <-- let everyone use this ID for now

print("imgur uploader v" + APP_VERSION + "\n")
config = os.path.join(os.getcwd(), "config.txt")
use_prev_album = False
try:
    with open(config, 'r') as file:
        lines = file.readlines()  # returns list of string TODO: handle when config file is messed up
        config_data = dict([tuple(line.strip().split("=")) for line in lines])
        client_id = config_data["CLIENT_ID"]
        album_title = input("Upload to previous album? Y/N")
        if album_title.upper() == "Y":
            use_prev_album = True

except FileNotFoundError:  # save the writing for later
    print("Config file not detected... Initializing config\n")
    print("Paste your imgur client ID here, leave blank if you want to modify the config.txt instead.\n")
    client_id = input("Enter Client ID: (v1.0 uses my account client ID) ")
    if client_id == '':
        # input("OK! Feel free to close the program")
        # exit()
        print("Using default demo ID...")
        client_id = DEFAULT_CLIENT_ID
except ValueError:
    input("Config file corrupted... Please fix or delete the config altogether.")
    exit()

if not use_prev_album:
    album_title = input("Enter a title for your new album: ")
    album_info = uploader.create_imgur_album(album_title, client_id)  # album_info is list [id (url), hash]
    if not album_info:  #if failed to create album
        exit()
else:
    album_info = [config_data["PREV_ALBUM_ID"], config_data["PREV_ALBUM_HASH"]]

album_url = "https://imgur.com/a/" + str(album_info[0])

print("\n(the link (and album hash) is also saved in albums.txt)")
with open(config, 'w') as f:
    f.write("CLIENT_ID=" + str(client_id)+ "\n")
    f.write("PREV_ALBUM_URL=" + album_url + "\n")
    f.write("PREV_ALBUM_HASH=" + str(album_info[1]) )
imageprocess.getfile(client_id, album_info[1])
print("After uploading, access your album at this link: " + album_url)
album_save_file = os.path.join(os.getcwd(), "albums.txt")
if not use_prev_album:
    with open(album_save_file, 'a') as savefile:
        savefile.write(f"Album title: {album_title}\nAlbum URL: {album_url}\nAlbum DeleteHash: {str(album_info[1])}\n\n")


exit_program = input("Operation Finished! Press any key to continue...")

exit()