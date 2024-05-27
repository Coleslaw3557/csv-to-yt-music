import csv
import time
import logging
import argparse
import json
from ytmusicapi import YTMusic
from requests.exceptions import RequestException

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Import CSV to YouTube Music Playlist')
parser.add_argument('csv_file', type=str, help='Path to the CSV file')
parser.add_argument('playlist_name', type=str, help='Name of the playlist to create')
parser.add_argument('added_songs_file', type=str, help='Path to the file to store added song IDs')
parser.add_argument('--retries', type=int, default=3, help='Number of retries for network requests')
parser.add_argument('--timeout', type=int, default=10, help='Timeout for network requests in seconds')
args = parser.parse_args()

# Initialize YTMusic with your headers
ytmusic = YTMusic('headers_auth.json')

# Read the CSV file
tracks = []

with open(args.csv_file, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        # Strip any leading/trailing spaces from the keys
        row = {k.strip(): v for k, v in row.items()}
        tracks.append(row)

# Debugging: Print the first row to check the keys
if tracks:
    logging.info(f"First row keys: {tracks[0].keys()}")

# Create a new playlist
playlist_id = ytmusic.create_playlist(args.playlist_name, "Imported from CSV")
logging.info(f"Playlist created with ID: {playlist_id}")

# Load added song IDs from file
try:
    with open(args.added_songs_file, 'r') as f:
        added_songs = set(json.load(f))
except FileNotFoundError:
    added_songs = set()

# Function to add items to the playlist with retry logic
def add_items_with_retry(playlist_id, song_id, retries=args.retries, delay=5):
    for attempt in range(retries):
        try:
            ytmusic.add_playlist_items(playlist_id, [song_id])
            logging.info(f"Added song ID {song_id} to playlist")
            return True
        except RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    logging.error(f"Failed to add song ID {song_id} after {retries} attempts")
    return False

# Function to like a song with retry logic
def like_song_with_retry(song_id, retries=args.retries, delay=5):
    for attempt in range(retries):
        try:
            ytmusic.rate_song(song_id, 'LIKE')
            logging.info(f"Liked song ID {song_id}")
            return True
        except RequestException as e:
            logging.warning(f"Attempt {attempt + 1} to like song failed: {e}")
            time.sleep(delay)
    logging.error(f"Failed to like song ID {song_id} after {retries} attempts")
    return False

# Search for each track and add to the playlist and liked music
for track in tracks:
    try:
        search_query = f"{track['Title']} {track['Artist']}"
        search_results = ytmusic.search(search_query, filter='songs')
        if search_results:
            song_id = search_results[0]['videoId']
            if song_id not in added_songs:
                if add_items_with_retry(playlist_id, song_id):
                    added_songs.add(song_id)
                    # Save the added song IDs to file
                    with open(args.added_songs_file, 'w') as f:
                        json.dump(list(added_songs), f)
                like_song_with_retry(song_id)
            else:
                logging.info(f"Song ID {song_id} already added, skipping")
        else:
            logging.warning(f"No results found for query: {search_query}")
    except KeyError as e:
        logging.error(f"KeyError: {e} in track: {track}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

logging.info(f"Playlist creation completed with ID: {playlist_id}")

