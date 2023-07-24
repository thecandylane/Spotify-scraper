import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
# from bs4 import BeautifulSoup
from pytube import YouTube
import os
from dotenv import load_dotenv
import requests
import urllib


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
YT_API = os.getenv("YT_API")


def authenticate_spotify(username, playlist_name):
    # Add your Spotify API credentials here
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    redirect_uri = REDIRECT_URI

    scope = 'user-library-read'

    # Redirect URI where the Spotify authorization code will be sent
    # token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    sp_oauth = spotipy.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)
    auth_url = sp_oauth.get_authorize_url()
    print(f"Please navigate here: {auth_url}")

    # Wait for the user to enter the authorization code
    code = input("Enter the authorization code: ")
    token_info = sp_oauth.get_access_token(code)

    token = token_info['access_token']

    if token:
        sp = spotipy.Spotify(auth=token)
        playlist = None
        playlists = sp.user_playlists(username)
        for pl in playlists['items']:
            if pl['name'] == playlist_name:
                playlist = pl
                break
        if playlist:
            return sp, playlist
        else:
            print("Playlist not found.")
            return None, None
    else:
        print("Authentication failed.")
        return None, None

def get_save_location():
    while True:
        file_path = input("Enter the file path or folder where you want to save the songs: ")
        if os.path.exists(file_path):
            return file_path
        else:
            print("Invalid path. Please enter a valid file path or folder.")

def get_youtube_link(song_title):
    query = urllib.parse.quote(song_title)
    api_key = YT_API
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return None

def download_song(youtube_link, song_title, save_location):
    yt = YouTube(youtube_link)
    yt.streams.filter(only_audio=True).first().download(output_path=save_location, filename=song_title)

def main():
    username = input("Enter your Spotify username: ")
    playlist_name = input("Enter the playlist name: ")

    # Authenticate with Spotify and get the playlist data
    sp, playlist = authenticate_spotify(username, playlist_name)
    if not sp or not playlist:
        return

    # Get the save location from the user
    save_location = get_save_location()

    # Process each song in the playlist
    for track in sp.playlist_tracks(playlist['id'])['items']:
        song_title = track['track']['name']
        print(song_title)
        # Search for the YouTube link for the song
        youtube_link = get_youtube_link(song_title)
        print(youtube_link)
        if youtube_link:
            print(f"Downloading {song_title}...")
            # Download the song as an mp3 file and save it to the chosen location
            download_song(youtube_link, song_title, save_location)
        else:
            print(f"Song not found: {song_title}")

if __name__ == "__main__":
    main()
