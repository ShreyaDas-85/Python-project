import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

# Declaring needed Variables
Spotifyusername = "username"
Year = input("What year you would like to travel to? Type the date in YYYY-MM-DD format:")
scope="scope"
redirect_uri="redirect url"
client_id="client id"
client_secret="client secret"
url = "url"+Year
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}

# SCRAPING BILLBOARD TOP 100 CHARTS WITH BEAUTIFUL SOUP
r = requests.get(url=url, headers=header)
soup = BeautifulSoup(r.text, "html.parser")
song_names_spans = soup.select("li ul li h3")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="scope",
        redirect_uri="url",
        client_id="client id",
        client_secret="client secret",
    )
)

song_urls = []
for song in song_names_spans:
    song_name = song.getText().strip()
    result = sp.search(q=song_name, type="track")

    if result["tracks"]["items"]:
        song_uri = result["tracks"]["items"][0]["uri"]
        song_urls.append(song_uri)
    else:
        print(f"Song {song_name} not found on Spotify")

# Creating a new playlist on Spotify
playlist_name = f"Billboard Hot 100 - {Year}"
description = "Top 100 songs on Billboard charts for the specified year."

playlist = sp.user_playlist_create(user=Spotifyusername,
                                   name=playlist_name,
                                   description=description,
                                   public=False)
# Adding songs to playlist

sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)
