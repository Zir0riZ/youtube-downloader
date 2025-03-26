# YouTube Video & Playlist Downloader

A Python-based YouTube video and playlist downloader using yt-dlp library.

## Features

- Download single YouTube videos
- Download complete YouTube playlists
- Batch download multiple playlists from a text file
- Auto-resume interrupted downloads
- Skip already downloaded videos
- Organize playlist videos in separate folders
- Support for 720p video quality

## Requirements

```python
pip install yt-dlp
```

## Usage

### Single Video or Playlist Download (bot.py)

Run the script and follow the interactive prompts:
```bash
python bot.py
```

Choose between:
1. Download a single video
2. Download a playlist

### Batch Playlist Download (playlist.py)

1. Create a `playlists.txt` file
2. Add playlist URLs (one per line)
3. Run:
```bash
python playlist.py
```

## Configuration

Default download settings:
- Video quality: 720p max
- Format: MP4
- Auto-retry on failure: 3 attempts
- Continues partial downloads
- Creates separate folders for playlists

## Error Handling

- Skips invalid videos in playlists
- Resumes interrupted downloads
- Reports download failures
- Verifies downloaded file integrity

## License

MIT License
