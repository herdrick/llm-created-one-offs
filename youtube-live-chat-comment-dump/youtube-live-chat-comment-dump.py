# usage: python youtube-live-chat-comment-dump.py > chat.txt

import requests
import time

# Replace with your YouTube API key
API_KEY = "AIzaSyBiJ_WY1KvqnHBryA1NTCX0kPFqvPcBAJM"

# Replace with your live chat ID (You can fetch this using the `liveBroadcasts` API)
# eh:  I got this with curl "https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id=X3NTqsoiloM&key=AIzaSyBiJ_WY1KvqnHBryA1NTCX0kPFqvPcBAJM"  ... where id is just from the video's URL https://www.youtube.com/watch?v=X3NTqsoiloM
#LIVE_CHAT_ID = "0ofMyAOAARpeQ2lrcUp3b1lWVU5EZGtaUk1EWmFiVzQxYlRaNmFUVjRhSGhyVEVwbkVndFlNMDVVY1hOdmFXeHZUUm9UNnFqZHVRRU5DZ3RZTTA1VWNYTnZhV3h2VFNBQk1BQSUzRDABggEICAQYAiAAKACIAQGgAdKs4Izh5ooDqAEAsgEA"
LIVE_CHAT_ID = "Cg0KC1gzTlRxc29pbG9NKicKGFVDQ3ZGUTA2Wm1uNW02emk1eGh4a0xKZxILWDNOVHFzb2lsb00"

# YouTube API endpoint for live chat messages
CHAT_MESSAGES_URL = "https://www.googleapis.com/youtube/v3/liveChat/messages"

# https://www.youtube.com/live_chat?continuation=0ofMyAOAARpeQ2lrcUp3b1lWVU5EZGtaUk1EWmFiVzQxYlRaNmFUVjRhSGhyVEVwbkVndFlNMDVVY1hOdmFXeHZUUm9UNnFqZHVRRU5DZ3RZTTA1VWNYTnZhV3h2VFNBQk1BQSUzRDABggEICAQYAiAAKACIAQGgAdKs4Izh5ooDqAEAsgEA&authuser=0


def fetch_live_chat_messages():
    """
    Fetch live chat messages from a YouTube live stream.
    """
    # Initial API request parameters
    params = {
        "liveChatId": LIVE_CHAT_ID,
        "part": "snippet,authorDetails",
        "key": API_KEY,
    }

    print("Fetching live chat messages...")
    while True:
        try:
            # Make the API request
            response = requests.get(CHAT_MESSAGES_URL, params=params)
            response.raise_for_status()  # Raise an error for HTTP failures

            # Parse the response
            data = response.json()
            items = data.get("items", [])
            next_page_token = data.get("nextPageToken", None)
            polling_interval = data.get("pollingIntervalMillis", 2000)  # Default 2 seconds

            # Print chat messages
            for item in items:
                message = item["snippet"]["displayMessage"]
                author = item["authorDetails"]["displayName"]
                print(f"{author}: {message}")

            # Break if no next page token (unlikely in live chat)
            if not next_page_token:
                break

            # Prepare for the next API request
            params["pageToken"] = next_page_token
            time.sleep(polling_interval / 1000.0)  # Convert milliseconds to seconds

        except Exception as e:
            print(f"Error fetching live chat messages: {e}")
            break

if __name__ == "__main__":
    fetch_live_chat_messages()
