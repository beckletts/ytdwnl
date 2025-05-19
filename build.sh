#!/bin/bash

# Install dependencies
npm install
pip install -r requirements.txt

# Install yt-dlp globally
pip install yt-dlp

# Create necessary directories
mkdir -p netlify/functions

# Copy the serverless function
cp netlify/functions/download.py netlify/functions/download.py

# Make the build script executable
chmod +x build.sh 