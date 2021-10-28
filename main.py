import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


data = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{data}"
SPOTIFY_ID = "450a8442dfd44e4cb55f2adc8d42f150"
SPOTIFY_SECRET = "5a4b467e706c419ca6af5194320c50b3"


response = requests.get(URL)
billboard_response = response.text
soup = BeautifulSoup(billboard_response, "html.parser")

# Pulling the data from web and adding the song to a list
song = soup.find_all(class_="chart-element__information__song text--truncate color--primary")
artist = soup.find_all(class_="chart-element__information__artist text--truncate color--secondary")
for item in song:
    songs_list = [item.text for item in song]

# Authenticate and generate token
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []
year = data.split("-")[0]

# Searching for the songs that I pulled from Billboard website and creating a song URI list
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)

# Generatig a playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{data} Billboard 100", public=False)
print(playlist)

# Adding the playlist to Spotify
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)