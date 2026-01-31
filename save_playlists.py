# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "spotipy",
#     "python-dotenv",
#     "tqdm",
# ]
# ///

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

DEFAULT_OUTPUT_PATH = Path.home() / "backups" / "spotify_playlists.json"

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Authenticate with Spotify
scope = "playlist-read-private"
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    open_browser=True,
    cache_path=Path.home() / ".spotify_cache"
)
sp = Spotify(auth_manager=auth_manager)

# Get current user's playlists
def get_user_playlists():
    playlists = []
    results = sp.current_user_playlists()
    
    while results:
        playlists.extend(results['items'])
        results = sp.next(results) if results['next'] else None

    return playlists

# Save playlists to a JSON file
def save_playlists_to_file(playlists, filename=DEFAULT_OUTPUT_PATH):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(playlists, f, ensure_ascii=False, indent=4)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, nargs="?", default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args()

# Main script
if __name__ == "__main__":
    args = parse_arguments()
    
    print("Fetching playlists...")
    playlists = get_user_playlists()
    
    # Prepare data to save (optional: save only names and tracks)
    playlists_data = []
    for playlist in tqdm(playlists):
        tracks = []
        results = sp.playlist_items(playlist['id'])
        while results:
            tracks.extend(results['items'])
            results = sp.next(results) if results['next'] else None
        
        playlists_data.append({
            "name": playlist['name'],
            "id": playlist['id'],
            "tracks": [{"name": track['track']['name'], "artist": track['track']['artists'][0]['name']} for track in tracks if track['track']]
        })

    # Save to file
    save_playlists_to_file(playlists_data, args.output)
    print(f"Playlists saved to '{args.output}'.")
