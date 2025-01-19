# VLC to Discord Rich Presence with Artwork Uploader

This project integrates VLC media player with Discord Rich Presence, providing live updates of the currently playing song on VLC, including metadata, progress, and artwork. The artwork is uploaded to a PHP server for accessibility and displayed in the Discord Rich Presence.

## Features
- Display song details (title, artist) in Discord Rich Presence.
- Show playback progress in the Rich Presence.
- Upload album artwork to a server and use it as the large image in Discord.
- Automatic updates every 15 seconds.

---

## Project Structure
### PHP Script (`api.php`)
The PHP script handles file uploads and serves the uploaded artwork. It performs:
- Password authentication for upload requests.
- File type validation (only images are allowed).
- Automatic cleanup of old images in the upload directory.
- Returns a public URL for uploaded images.

### Python Script (`vlc_to_discord.py`)
The Python script:
- Fetches the currently playing song's metadata from VLC's web interface.
- Uploads album artwork to the PHP server.
- Updates Discord Rich Presence with song details, playback progress, and artwork.

---

## Installation

### Prerequisites
1. **PHP Server**:
   - A server with PHP 7.0+ installed.
   - Ability to upload and serve files (e.g., Apache, Nginx).
2. **Python**:
   - Python 3.7+ installed.
   - Install required packages:
     ```bash
     pip install requests pypresence
     ```
3. **VLC Media Player**:
   - Ensure VLC is installed and its web interface is enabled.
   - Default VLC web interface URL: `http://127.0.0.1:8080`.

### Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/NullRien/VlcDiscordPresence.git
   cd VlcDiscordPresence
   ```

2. **Configure PHP Server**:
   - Place `api.php` in your PHP server's root directory.
   - Update the password in `api.php`:
     ```php
     define('UPLOAD_PASSWORD', 'your_secure_password');
     ```

3. **Configure VLC**:
   - Enable VLC's web interface:
     - Open VLC -> Tools -> Preferences -> (set show settings to all) -> Interface -> Main Interfaces.
     - Check the box for "Web."
   - Set a password for the VLC web interface:
     - Navigate to `Main Interfaces -> Lua`.
     - Set a password in the "Lua HTTP" section.

4. **Update Python Script**:
   - Update the following variables in `main.py`:
     ```python
     RPC_CLIENT_ID = "your_discord_app_client_id"
     UPLOAD_URL = "https://your-server.com/api.php"
     UPLOAD_PASSWORD = "your_secure_password"
     vlc_password = "your_vlc_password"
     ```

---

## Usage
1. **Run VLC Media Player**:
   - Start playing a song in VLC.

2. **Start the Python Script**:
   ```bash
   python vlc_to_discord.py
   ```

3. **Check Discord**:
   - Your Rich Presence should now show the current song, playback progress, and album artwork.

---

## Security
- **PHP Script**:
  - Password-protects file uploads to prevent unauthorized access.
  - Validates file types to allow only images.

- **Python Script**:
  - Avoid storing sensitive passwords directly in the script. Use environment variables or a configuration file if possible.

---

## Troubleshooting
- **No artwork displayed**:
  - Ensure VLC's web interface is enabled and accessible.
  - Verify the artwork URL is valid.
- **Server errors**:
  - Check PHP error logs for detailed information.
- **Discord Rich Presence not updating**:
  - Verify that the Discord app is running and connected.

---

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests to enhance the project.

---

## Notes
This script may need to be edited to work on your system, if anyone wants to actually use this i will update it in the future to be more user friendly.
