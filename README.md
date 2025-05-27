<a href="https://www.hannahilea.com/blog/houseplant-programming">
  <img alt="Static Badge" src="https://img.shields.io/badge/%F0%9F%AA%B4%20Houseplant%20-x?style=flat&amp;label=Project%20type&amp;color=1E1E1D">
</a>

# Spotify Playlist Backup

A self-contained Python script to backup all your Spotify playlists to a JSON file.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed
- Spotify API credentials (see setup below)

## Setup

- Create a Spotify app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

- Edit `.env` with your actual values.

## Usage

Simply run the script with uv:

```bash
uv run save_playlists.py
```

Or specify a custom output path:

```bash
uv run save_playlists.py /path/to/your/backup.json
```

The script will:
- Automatically install required dependencies
- Fetch all your playlists
- Save them to `~/backups/spotify_playlists.json` (default) or your specified path

## Features

- **Self-contained**: No need to manage virtual environments or install dependencies manually
- **Progress tracking**: Shows progress bar while fetching playlists
- **Complete backup**: Saves playlist names, IDs, and track details (name and artist)

## Output

The script creates a JSON file with the following structure:

```json
[
  {
    "name": "My Playlist",
    "id": "playlist_id",
    "tracks": [
      {
        "name": "Song Title",
        "artist": "Artist Name"
      }
    ]
  }
]
``` 
