import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import unquote, urlparse
from pypresence import Presence
import time
import os
import xml.etree.ElementTree as ET

# Variables
RPC_CLIENT_ID = "1298376685147789654"  # Replace with your Discord application's client ID
UPLOAD_URL = "https://yourdomain.com/song/api.php"  # Replace with your server URL
UPLOAD_PASSWORD = "secure_password"  # Same password as in the PHP script

last_song = None
image_key = None
uploaded_images = {}

# Function to get the local file path from the VLC artwork URL
def get_local_file_path(file_uri):
    parsed = urlparse(file_uri)
    return unquote(parsed.path)

# Function to upload the artwork to the PHP server
def upload_artwork(file_path):
    if not os.path.exists(file_path):
        print(f"Artwork file does not exist: {file_path}")
        return None
    
    with open(file_path, "rb") as img_file:
        try:
            response = requests.post(
                UPLOAD_URL,
                data={"password": UPLOAD_PASSWORD},
                files={"image": img_file}
            )
            if response.status_code == 200:
                result = response.json()
                if result["status"]:
                    print(f"Uploaded artwork: {result['url']}")
                    return result["url"]  # Use this URL in RPC updates
                else:
                    print(f"Failed to upload artwork: {result['message']}")
            else:
                print(f"Server error: {response.status_code}")
        except Exception as e:
            print(f"Error uploading artwork: {e}")
    return None

# Function to fetch music info from VLC
def get_music_info(username="", password=""):
    url = "http://127.0.0.1:8080/requests/status.xml"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            meta = root.find(".//category[@name='meta']")
            position = root.findtext('position')
            length = root.findtext('length')
            artist = meta.findtext("info[@name='artist']") if meta else "Unknown"
            title = meta.findtext("info[@name='title']") if meta else "Unknown"
            artwork_url = meta.findtext("info[@name='artwork_url']") if meta else None
            # Convert position and length to readable format
            current_position_sec = float(position) * float(length)
            current_position_min = int(current_position_sec // 60)
            current_position_sec = int(current_position_sec % 60)
            length_min = int(int(length) // 60)
            length_sec = int(int(length) % 60)
            pos = f"{current_position_min}:{current_position_sec:02d}/{length_min}:{length_sec:02d}"
            
            return {"artist": artist, "title": title, "artwork_url": artwork_url, "pos": pos}
        else:
            print(f"Failed to fetch music info: {response.status_code}")
    except Exception as e:
        print(f"Error fetching music info: {e}")
    return None

# Function to update Discord Rich Presence
def update_discord_presence(rpc, artist, title, image_key, pos):
    try:
        rpc.update(
            activity_type = 2,
            details=f"{title}",
            state=f"By {artist}",
            large_image=image_key,
            large_text=pos,
            start=None,
            end=None,
        )
        print(f"RPC updated: {title} by {artist}")
    except Exception as e:
        print(f"Error updating RPC: {e}")

# Main program
if __name__ == "__main__":
    # Connect to Discord Rich Presence
    rpc = Presence(RPC_CLIENT_ID)
    rpc.connect()

    # VLC password (if required)
    vlc_password = ""

    while True:
        music_info = get_music_info(vlc_username, vlc_password)

        if music_info:
            artist = music_info["artist"]
            title = music_info["title"]
            artwork_url = music_info["artwork_url"]
            pos = music_info["pos"]

            # Check if the song has changed
            current_song = f"{artist} - {title}"
            if current_song != last_song:
                print(f"Song changed: {current_song}")
                last_song = current_song

                # Handle artwork upload
                if artwork_url:
                    local_path = get_local_file_path(artwork_url)
                    if current_song not in uploaded_images:
                        uploaded_image = upload_artwork(local_path)
                        if uploaded_image:
                            uploaded_images[current_song] = uploaded_image
                        else:
                            uploaded_images[current_song] = None

                # Update RPC with the uploaded image or default
                image_key = uploaded_images.get(current_song, "default_image")
                update_discord_presence(rpc, artist, title, image_key, pos)
            else:
                update_discord_presence(rpc, artist, title, image_key, pos)
                print(f"No song change detected. Current song: {current_song}")
        else:
            print("No music playing or failed to fetch music info.")

        time.sleep(15)  # Update every 15 seconds
