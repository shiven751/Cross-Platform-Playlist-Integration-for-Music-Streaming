
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests


# Spotif-y API credentials
SPOTIFY_CLIENT_ID = "246791f8c8514436aa34a4ce9100755f"
SPOTIFY_CLIENT_SECRET = "577f0cd8e4f64cb7adcc38d606fa3a1b"

# Spotify setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# YouTube API setup
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES) # Here, replace the path with your cliet secrets json file
credentials = flow.run_local_server(port=0)
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {credentials.token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
})




# Function to create a YouTube playlist
def create_youtube_playlist(title, description=""):
    url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet"
    body = {
        "snippet": {
            "title": title,
            "description": description
        }
    }
    try:
        response = session.post(url, json=body)
        response.raise_for_status()
        data = response.json()
        playlist_id = data.get("id")
        if playlist_id:
            print(f"Created YouTube playlist with ID: {playlist_id}")
            return playlist_id
        else:
            print("Failed to create playlist.")
            return None
    except Exception as e:
        print(f"Error creating YouTube playlist: {e}")
        return None




# the one which is updated and is now functional 




# Function to search YouTube for a video with "Artist - Song Title" format

YOUTUBE_API_KEY = "AIzaSyA9Bg6ND8QMxHvd5Xr-IB74pdN-LMvVbCU"

def search_youtube_video_id(track_name, artist_name):
    query = f"{artist_name} - {track_name}"  # Format the query as "Artist - Song Title"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}"
    
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Get the video ID of the first search result
        video_id = data["items"][0]["id"]["videoId"] if data["items"] else None
        return video_id
    
    except Exception as e:
        print(f"Error searching YouTube for video: {e}")
        return None



# Function to add a video to a YouTube playlist
def add_video_to_playlist(playlist_id, video_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
    body = {
        "snippet": {
            "playlistId": playlist_id,  # Playlist ID where video will be added
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id  # Video ID to add to the playlist
            }
        }
    }
    try:
        response = session.post(url, json=body)
        response.raise_for_status()  # Will raise an error for bad responses
        print(f"Video with ID {video_id} added to playlist with ID {playlist_id}")
    except Exception as e:
        print(f"Error adding video to playlist: {e}")









# Test function to fetch tracks from a Spotify playlist
def test_spotify_connection(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
        tracks = []
        for item in results["items"]:
            track = item["track"]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            print(f"Track Name: {track_name} by {artist_name}")
            tracks.append((track_name, artist_name))
        print("Spotify API connection successful.")
        return tracks  # Return list of tracks
    except Exception as e:
        print(f"Error connecting to Spotify API: {e}")
        return []



# Replace with your actual Spotify playlist ID
playlist_id = "4Ng1D8OHGRnHd9vccPFW6G"                      # make sure this is 22 characters long
tracks = test_spotify_connection(playlist_id)

# Create a YouTube playlist
youtube_playlist_id = create_youtube_playlist("Playlist created without human intervention", "A playlist created via the YouTube API")

if youtube_playlist_id:
    # Search for each track on YouTube and add it to the playlist
    for track_name, artist_name in tracks:
        video_id = search_youtube_video_id(track_name, artist_name)
        if video_id:
            add_video_to_playlist(youtube_playlist_id, video_id)
        else:
            print(f"No video found for {track_name} by {artist_name} on YouTube.")


