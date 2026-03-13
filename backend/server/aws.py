import boto3
import requests
import os
import json
from datetime import datetime
from globals import USERNAME

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
    def __init__(self):
        """
        Initialize an S3 client using credentials from environment variables.
        """

        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        self.bucket_name = AWS_S3_BUCKET
        self.session_file = f"{USERNAME}/SESSION_{USERNAME}.json"

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

    def get_presigned_url(self, file_path, session_id=None):
        """
        Ask the local Flask API to generate a presigned upload URL.
        """
        url = f"{LOCAL_API_BASE_URL}/generate-presigned-url"

        payload = {
            "file_name": os.path.basename(file_path),
            "username": USERNAME,
        }

        if session_id:
            payload["session_id"] = session_id

        response = requests.post(url, json=payload)
        response.raise_for_status()

        return response.json()["url"]

    # ----------------------------
    # Session tracking
    # ----------------------------

    def create_session(self, app_name, user_with):
        try:
            now = datetime.now().isoformat()
            session_entry = {
                "app_name": app_name,
                "user_with": user_with,
                "start_timestamp": now,
                "end_timestamp": None,
                "status": "active"
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
            print(f"Error creating session: {e}")
            return False

    def update_session(self, session_id):
        try:
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

            # Update the most recent active session with new timestamp
            if existing_data:
                for session in reversed(existing_data):
                    if session.get("status") == "active":
                        session["end_timestamp"] = datetime.now().isoformat()
                        break

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

            # Return the latest active session (skip ended sessions)
            for session in reversed(session_data):
                if session.get("status") != "ended":
                    return session
            
            # If all sessions are ended, return an empty session
            return {"app_name": None, "user_with": None}

        except self.client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            print(f"Error getting latest session: {e}")
            return None

    def get_all_sessions(self):
        """
        Get all sessions from the session file.
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.session_file,
            )

            session_data = json.loads(
                response["Body"].read().decode("utf-8")
            )

            if not session_data:
                return []

            return session_data

        except self.client.exceptions.NoSuchKey:
            return []
        except Exception as e:
            print(f"Error getting all sessions: {e}")
            return []
    
    def end_session(self):
        try:
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

            # Mark the most recent active session as ended
            if existing_data:
                for session in reversed(existing_data):
                    if session.get("status") == "active":
                        session["end_timestamp"] = datetime.now().isoformat()
                        session["status"] = "ended"
                        break

            self.client.put_object(
                Bucket=self.bucket_name,
                Key=self.session_file,
                Body=json.dumps(existing_data),
                ContentType="application/json",
            )

            return True

        except Exception as e:
            print(f"Error ending session: {e}")
            return False

    def delete_file(self, file_key):
        """
        Delete a file from S3 by its key.
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            return True
        except Exception as e:
            print(f"Error deleting file from S3: {e}")
            return False