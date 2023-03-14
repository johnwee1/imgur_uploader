import requests
import json
import os

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


async def upload_image(session, filepath, client_id, album_hash):

    url = 'https://api.imgur.com/3/image'

    with open(filepath, 'rb') as img_file:
        payload = {'image': img_file.read(),
               'album': album_hash,
        }

    headers = {
        'Authorization': 'Client-ID ' + client_id
    }
    
    async with session.post(url, headers=headers, data=payload) as response:
        if response.ok:
            print("Upload success: " + filepath)
            try:
                print(await response.json())
                print("\n")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}\n")
        else:
            print(f"Upload failed, status: {response.status} {response.reason}")
        
    # Delete the compressed photo 
    os.remove(filepath)  
