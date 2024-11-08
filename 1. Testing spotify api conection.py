import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

# Spotify API credentials
SPOTIFY_CLIENT_ID = "246791f8c8514436aa34a4ce9100755f"
SPOTIFY_CLIENT_SECRET = "577f0cd8e4f64cb7adcc38d606fa3a1b"

# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Test function to fetch tracks from a Spotify playlist
def test_spotify_connection(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
        for item in results["items"]:
            track = item["track"]
            print(f"Track Name: {track['name']} by {track['artists'][0]['name']}")
        print("Spotify API connection successful.")
    except Exception as e:
        print(f"Error connecting to Spotify API: {e}")



# Replace with your actual Spotify playlist ID
playlist_id = "5mInjqr1YaWunIobhZ7SmM"
test_spotify_connection(playlist_id)
print(len(playlist_id))

