#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

def download_video(url, output_dir="."):
    """
    Download a YouTube video at 320p quality using yt-dlp.
    
    Args:
        url (str): The YouTube video URL
        output_dir (str): Directory to save the downloaded video
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Format the command to download the video at 320p quality
        command = [
            "yt-dlp",
            "-f", "best[height<=320]",  # Select format with height <= 320p
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url
        ]
        
        # Execute the command
        print(f"Downloading video from {url} at 320p quality...")
        subprocess.run(command, check=True)
        print("Download completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos at 320p quality")
    parser.add_argument("url", help="YouTube video URL to download")
    parser.add_argument("-o", "--output", default="downloads", help="Output directory (default: ./downloads)")
    args = parser.parse_args()
    
    download_video(args.url, args.output)

if __name__ == "__main__":
    main() 