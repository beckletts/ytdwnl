# YouTube 320p Downloader

A simple application to download YouTube videos at 320p quality (or other quality options).

## Features

- Download YouTube videos at various quality options (320p, 480p, 720p, 1080p)
- Command-line interface
- Web interface for easier use
- Simple and user-friendly design

## Requirements

- Python 3.6 or higher
- yt-dlp package
- Flask (for web interface)

## Installation

1. Clone this repository or download the files
2. Set up a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage - Command Line Interface

To download a YouTube video at 320p quality using the command-line interface:

```bash
# Make sure your virtual environment is activated
python3 youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

By default, videos will be saved to a `downloads` directory. To specify a different output directory:

```bash
python3 youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/directory
```

## Usage - Web Interface

To run the web interface:

```bash
# Make sure your virtual environment is activated
python3 app.py
```

Then open your browser and go to:

```
http://localhost:8080
```

The web interface allows you to:
1. Enter a YouTube video URL
2. Select the desired quality (320p, 480p, 720p, 1080p)
3. Download the video with a user-friendly interface

## Notes

- If your selected quality isn't available, the app will download the next best quality that's no higher than your selection.
- This tool is for personal use only. Please respect YouTube's terms of service. 