import boto3
import requests
import os
import json
from datetime import datetime

# ----------------------------
# Environment configuration
# ----------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "digital-diary")
LOCAL_API_BASE_URL = os.getenv("LOCAL_API_BASE_URL", "http://127.0.0.1:5000")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise RuntimeError(
        "Missing AWS credentials. "
        "Make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in your .env file."
    )


class S3:
    def __init__(self, username=None):
        """
        Initialize an S3 client using credentials from environment variables.
        
        Args:
            username: Optional username for session file naming. If not provided, defaults to generic session naming.
        """

        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        self.bucket_name = AWS_S3_BUCKET
        self.username = username
        self.session_file = f"SESSION_{username}.json" if username else "SESSION_default.json"

    # ----------------------------
    # Bucket helpers
    # ----------------------------

    def bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            return True
        except self.client.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def create(self):
        if self.bucket_exists():
            print("Bucket already exists:", self.bucket_name)
        else:
            self.client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
            )

    def get(self):
        return self

    # ----------------------------
    # Presigned URL helpers
    # ----------------------------

    def get_presigned_url(self, file_path, game_id=None):
        """
        Ask the local Flask API to generate a presigned upload URL.
        """
        url = f"{LOCAL_API_BASE_URL}/generate-presigned-url"

        payload = {
            "file_name": os.path.basename(file_path),
            "username": self.username,
        }

        if game_id:
            payload["game_id"] = game_id

        response = requests.post(url, json=payload)
        response.raise_for_status()

        return response.json()["url"]

    # ----------------------------
    # Session tracking
    # ----------------------------

    def update_session(self, game_id):
        try:
            session_entry = {
                "game_id": game_id,
                "timestamp": datetime.now().isoformat(),
            }

            try:
                response = self.client.get_object(
                    Bucket=self.bucket_name,
                    Key=self.session_file,
                )
                existing_data = json.loads(
                    response["Body"].read().decode("utf-8")
                )
                if not isinstance(existing_data, list):
                    existing_data = []
            except self.client.exceptions.NoSuchKey:
                existing_data = []

            existing_data.append(session_entry)

            self.client.put_object(
                Bucket=self.bucket_name,
                Key=self.session_file,
                Body=json.dumps(existing_data),
                ContentType="application/json",
            )

            return True

        except Exception as e:
            print(f"Error updating session: {e}")
            return False

    def get_latest_session(self):
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.session_file,
            )

            session_data = json.loads(
                response["Body"].read().decode("utf-8")
            )

            if not session_data:
                return None

            return session_data[-1]

        except self.client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            print(f"Error getting latest session: {e}")
            return None

    # ----------------------------
    # User helpers
    # ----------------------------

    def user_exists(self, username):
        """
        Check if a user exists in S3 by checking for their session file.
        Returns True if the user has any data in S3, False otherwise.
        """
        try:
            session_key = f"SESSION_{username}.json"
            self.client.head_object(Bucket=self.bucket_name, Key=session_key)
            return True
        except self.client.exceptions.NoSuchKey:
            return False
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False
