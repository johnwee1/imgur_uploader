# imgur_uploader
Light python script that compresses JPEGs and uploads to imgur

## Features
- Enter your personal client ID or use the one that I made (no configuration necessary!)
- Upload all photos in directory as an album without having to sign in
- Creates a compressed image, uploads it, then deletes it. Your photos remain safe!
- Creates a config file that allows you to upload to a previously used album, and creates an albums.txt file that keeps track of all the albums created

## How to use
- Download and install dependencies outlined in `requirements.txt` - it's really just `requests` and `Pillow`.
- Run main.py


## TODO:
- Asynchronous requests
- Specify granular quality setting
- Specify config.txt and albums.txt location
- Delete albums given the album's deleteHash
