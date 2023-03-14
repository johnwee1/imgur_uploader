import requests
import base64
import os
import json

# client_id = 'ae33cb66617c656'  # Actually there is no need for a Bearer token, just need client ID is all!!
# album_hash = '5259359i3'  # Create a new anon album everytime this code is run?

def create_imgur_album(album_title, client_id):
    payload = {'title': album_title,
               'description': 'Album created by imgur uploader',
               }
    files = [
    ]
    headers = {
        'Authorization': 'Client-ID ' + str(client_id)
    }

    response_raw = requests.request("POST", "https://api.imgur.com/3/album", headers=headers, data=payload, files=files)
    try:
        response = response_raw.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}\n")
        return
    if (response["status"] != 200):
        print("Album creation failed status: " + str(response["status"]))
        return False
    else:
        return [response["data"]["id"], response["data"]["deletehash"]]


def upload_image(filepath, client_id, album_hash):
    with open(filepath, 'rb') as img_file:
        encoded_bytes = base64.b64encode(img_file.read())
    payload = {'image': encoded_bytes,
               'album': album_hash}
    files = []
    headers = {
        'Authorization': 'Client-ID ' + client_id,
    }

    response_raw = requests.request("POST", "https://api.imgur.com/3/image", headers=headers, data=payload, files=files)
    try:
        response = response_raw.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}\n")
        return False

    if response["success"]:
        print("Upload success: " + filepath + "\n")
        print(response)
        return True
        # return imgur link to album not here
    else:
        print("Upload failed, status: " + response["status"])
        return False


