import os
import imageprocess
import uploader
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

APP_VERSION = "1.0"
DEFAULT_CLIENT_ID = "ae33cb66617c656" # <-- let everyone use this ID for now
IMGUR_ALBUM_URL = "https://imgur.com/a/"

async def main():
    print("imgur uploader v" + APP_VERSION + "\n")
    config = os.path.join(os.getcwd(), "config.txt")
    use_prev_album = False
    try:
        with open(config, 'r') as file:
            lines = file.readlines()  # returns list of string TODO: handle when config file is messed up
            config_data = dict([tuple(line.strip().split("=")) for line in lines])
            client_id = config_data["CLIENT_ID"]
            if input("Upload to previous album? Y/N\n").upper() == "Y":
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
        album_info = uploader.create_imgur_album(album_title, client_id)  # album_info is list [id, hash]
        if not album_info:  #if failed to create album
            exit()
    else:
        album_info = [config_data["PREV_ALBUM_ID"], config_data["PREV_ALBUM_HASH"]]

    album_url = IMGUR_ALBUM_URL + str(album_info[0])

    print("\n(the link (and album hash) is also saved in albums.txt)")
    with open(config, 'w') as f:
        f.write("CLIENT_ID=" + str(client_id)+ "\n")
        f.write("PREV_ALBUM_ID=" + str(album_info[0]) + "\n")
        f.write("PREV_ALBUM_HASH=" + str(album_info[1]) )

    with ThreadPoolExecutor() as executor:
        cp_paths = executor.map(imageprocess.compress_img, imageprocess.getfiles())

    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for path in cp_paths:
                tg.create_task(uploader.upload_image(session, path, client_id, album_info[1]))

    print(f"After uploading, access your album at this link: {album_url} \n")
    album_save_file = os.path.join(os.getcwd(), "albums.txt")
    if not use_prev_album:
        with open(album_save_file, 'a') as savefile:
            savefile.write(f"Album title: {album_title}\n"
                           f"Album URL: {album_url}\n"
                           f"Album DeleteHash: {str(album_info[1])}\n\n")


    print("Operation Finished!")

    exit()

asyncio.run(main())