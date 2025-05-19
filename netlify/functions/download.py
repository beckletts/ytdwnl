import json
import os
import subprocess
import uuid
import tempfile
from http.server import BaseHTTPRequestHandler

def download_video(url, quality=320):
    """Download a YouTube video at specified quality using yt-dlp."""
    try:
        # Create a temporary directory for the download
        temp_dir = tempfile.mkdtemp()
        output_template = f"{temp_dir}/%(title)s.%(ext)s"
        
        # Format the command to download the video at specified quality
        command = [
            "yt-dlp",
            "-f", f"best[height<={quality}]",
            "-o", output_template,
            "--no-playlist",
            url
        ]
        
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Find the downloaded file
        files = os.listdir(temp_dir)
        
        if not files:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Download completed but no file was found"})
            }
        
        # Get the file path
        file_path = os.path.join(temp_dir, files[0])
        
        # Read the file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Clean up
        os.remove(file_path)
        os.rmdir(temp_dir)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "video/mp4",
                "Content-Disposition": f"attachment; filename={files[0]}"
            },
            "body": file_content,
            "isBase64Encoded": True
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error downloading video: {e.stderr}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
        }

def handler(event, context):
    """Netlify serverless function handler."""
    if event["httpMethod"] != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method not allowed"})
        }
    
    try:
        body = json.loads(event["body"])
        url = body.get("url", "").strip()
        quality = int(body.get("quality", 320))
        
        if not url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Please provide a YouTube URL"})
            }
        
        if not ("youtube.com" in url or "youtu.be" in url):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Please provide a valid YouTube URL"})
            }
        
        return download_video(url, quality)
        
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
        } 