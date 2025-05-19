const axios = require('axios');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const util = require('util');

const execPromise = util.promisify(exec);

exports.handler = async function(event, context) {
  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { url, quality = 320 } = JSON.parse(event.body);

    if (!url) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Please provide a YouTube URL' })
      };
    }

    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Please provide a valid YouTube URL' })
      };
    }

    // Create a temporary directory
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'yt-'));
    const outputTemplate = path.join(tempDir, '%(title)s.%(ext)s');

    // Download the video using yt-dlp
    const command = `yt-dlp -f "best[height<=${quality}]" -o "${outputTemplate}" --no-playlist "${url}"`;
    
    try {
      await execPromise(command);
    } catch (error) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: `Error downloading video: ${error.message}` })
      };
    }

    // Find the downloaded file
    const files = fs.readdirSync(tempDir);
    
    if (files.length === 0) {
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'Download completed but no file was found' })
      };
    }

    const filePath = path.join(tempDir, files[0]);
    const fileContent = fs.readFileSync(filePath);
    
    // Clean up
    fs.unlinkSync(filePath);
    fs.rmdirSync(tempDir);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'video/mp4',
        'Content-Disposition': `attachment; filename="${files[0]}"`
      },
      body: fileContent.toString('base64'),
      isBase64Encoded: true
    };

  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: `An unexpected error occurred: ${error.message}` })
    };
  }
}; 