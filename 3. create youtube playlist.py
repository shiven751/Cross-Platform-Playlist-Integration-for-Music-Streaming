import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# Step 1: Authentication and OAuth flow
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
credentials = flow.run_local_server(port=0)

# Step 2: Use the authorized credentials
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
            return playlist_id  # Return playlist ID for later use
        else:
            print("Failed to create playlist.")
            return None
    except Exception as e:
        print(f"Error creating YouTube playlist: {e}")
        return None













# Function to add a video to a playlist
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

# Step 3: Create a playlist and add a video to it
playlist_id = create_youtube_playlist("My Test Playlist", "A playlist created via the YouTube API")
if playlist_id:
    # Step 4: Add a video to the newly created playlist
    # Replace 'VIDEO_ID' with an actual YouTube video ID
    video_id = "dQw4w9WgXcQ"  # Example video ID, replace with the actual ID
    add_video_to_playlist(playlist_id, video_id)
