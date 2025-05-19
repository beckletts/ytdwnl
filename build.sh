#!/bin/bash

# Install dependencies
npm install
pip install -r requirements.txt

# Install yt-dlp globally
pip install yt-dlp

# Create necessary directories
mkdir -p netlify/functions

# Make the build script executable
chmod +x build.sh 