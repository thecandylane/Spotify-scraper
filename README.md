# Spotify-scraper
# Spotify to YouTube Downloader

This script lets you download songs from your Spotify playlist as MP3 files from YouTube.

## Setup

once the repo is cloned, start your virtual env. 
install necessary requirements. 'pip install -r requirements.txt'

## Configuration

To use the script, you need to set several environment variables:

- `CLIENT_ID`: Your Spotify Client ID.
- `CLIENT_SECRET`: Your Spotify Client Secret.
- `REDIRECT_URI`: Your Spotify App's Redirect URI. (recommend setting this to http://localhost:8080 on both dashboard and env var.)
- ^ All 3 of these are on your Spotify developer dashboard. All are free to create. 
- `YT_API`: Your YouTube Data API key. (easy to acquire, keep in mind it's quota. could be done using beautiful soup but I didn't want an IP ban risk)  

You can set these variables in a `.env` file in the project's root directory.

## Usage

Run the script using the following command:
'python main.py'

You will be prompted to enter your Spotify username and the name of the playlist you wish to download. After that, you will be asked to authenticate your Spotify account by navigating to a provided URL and pasting the redirected code within the new URL back into the console.

Next, you'll be asked to provide the directory where the downloaded songs will be saved.

Finally, the script will start to download each song from the provided playlist as an MP3 file and save them to the specified directory.
