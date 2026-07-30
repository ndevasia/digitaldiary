#!/usr/bin/env python3
"""
Download user folders from S3 digital-diary bucket locally.
"""

import boto3
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Environment configuration
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "digital-diary")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise RuntimeError(
        "❌ Missing AWS credentials.\n"
        "Please ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set.\n\n"
        "Options:\n"
        "1. Create/update .env file in the project root with:\n"
        "   AWS_ACCESS_KEY_ID=your_key\n"
        "   AWS_SECRET_ACCESS_KEY=your_secret\n"
        "2. Or set environment variables before running this script"
    )

# Users to download
USERS = [
    "Kahi",
    "Gumi",
    "Kyla",
    "Murtaza",
    "Ruqaiya",
    "Anna",
    "Catherine",
    "dylychill",
    "Sabrina",
    "Teyah",
    "Irene", 
    "Daniel"
]

# Local output directory
OUTPUT_DIR = Path("s3_data")


def download_user_folder(s3_client, username):
    """
    Download all objects under a user's S3 prefix to local folder.
    """
    user_output_dir = OUTPUT_DIR / username
    user_output_dir.mkdir(parents=True, exist_ok=True)
    
    prefix = f"{username}/"
    downloaded_count = 0
    
    try:
        # List all objects under the user's prefix
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=AWS_S3_BUCKET, Prefix=prefix)
        
        for page in pages:
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                # Skip the prefix itself if it appears as an object
                if key == prefix:
                    continue
                
                # Calculate local file path (remove username prefix)
                relative_key = key[len(prefix):]
                local_path = user_output_dir / relative_key
                
                # Create subdirectories if needed
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Skip if file already exists
                if local_path.exists():
                    print(f"Skipping {key} (already exists)")
                    continue
                
                # Download the file
                print(f"Downloading {key}...")
                s3_client.download_file(AWS_S3_BUCKET, key, str(local_path))
                downloaded_count += 1
        
        print(f"✓ Downloaded {downloaded_count} files for user '{username}' to {user_output_dir}")
        return downloaded_count
        
    except Exception as e:
        print(f"✗ Error downloading folder for user '{username}': {e}")
        return 0


def main():
    """
    Main function to download all user folders.
    """
    print(f"Starting S3 download for {len(USERS)} users...")
    print(f"Bucket: {AWS_S3_BUCKET}")
    print(f"Region: {AWS_REGION}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 60)
    
    # Create S3 client
    s3_client = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    
    # Download each user's folder
    total_files = 0
    for username in USERS:
        print(f"\nDownloading user: {username}")
        files_count = download_user_folder(s3_client, username)
        total_files += files_count
    
    print("-" * 60)
    print(f"\nDownload complete!")
    print(f"Total files downloaded: {total_files}")
    print(f"Data saved to: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()
