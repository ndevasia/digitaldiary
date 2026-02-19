#!/bin/bash

# FFmpeg installation script for macOS 64-bit
# Downloads and installs FFmpeg to bin/mac/x64

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET_DIR="$SCRIPT_DIR/mac/x64"
TEMP_DIR=$(mktemp -d)

echo "Installing FFmpeg to $TARGET_DIR..."

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

# Download FFmpeg
echo "Downloading FFmpeg..."
cd "$TEMP_DIR"
curl -L -o ffmpeg.zip "https://evermeet.cx/ffmpeg/ffmpeg-8.0.1.zip"

# Extract
echo "Extracting FFmpeg..."
unzip -q ffmpeg.zip

# Find and copy ffmpeg binary
echo "Installing ffmpeg..."
ffmpeg_binary=$(find . -name "ffmpeg" -type f | head -n 1)

if [ -z "$ffmpeg_binary" ]; then
    echo "Error: ffmpeg not found in the downloaded package"
    rm -rf "$TEMP_DIR"
    exit 1
fi

cp "$ffmpeg_binary" "$TARGET_DIR/ffmpeg"
chmod +x "$TARGET_DIR/ffmpeg"

# Cleanup
cd /
rm -rf "$TEMP_DIR"

echo "FFmpeg installed successfully at $TARGET_DIR/ffmpeg"
