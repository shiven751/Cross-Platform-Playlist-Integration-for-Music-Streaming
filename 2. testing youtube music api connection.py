import requests

# YouTube API key
YOUTUBE_API_KEY = "AIzaSyA9Bg6ND8QMxHvd5Xr-IB74pdN-LMvVbCU"

# Test function to search for a song on YouTube
def test_youtube_connection(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors in the request
        data = response.json()
        if data.get("items"):
            video_id = data["items"][0]["id"]["videoId"]
            print(f"Found video ID: {video_id} for '{song_name}' by '{artist_name}'")
        else:
            print(f"No video found for '{song_name}' by '{artist_name}'")
    except Exception as e:
        print(f"Error connecting to YouTube API: {e}")

# Test search
test_youtube_connection("Blinding Lights", "The Weeknd")






