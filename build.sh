#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p netlify/functions

# Copy the serverless function
cp netlify/functions/download.py netlify/functions/download.py

# Make the build script executable
chmod +x build.sh 