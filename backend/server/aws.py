import boto3
import requests
import os
import json
from datetime import datetime


def get_default_username():
    """Get the default username (user 0) from user.json"""
    try:
        # Find user.json in the model directory
        model_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'backend', 'model'
        )
        user_json_path = os.path.join(model_dir, 'user.json')
        
        if os.path.exists(user_json_path):
            with open(user_json_path, 'r') as f:
                data = json.load(f)
            users = data.get('users', [])
            # Find user with user_id = 0
            for user in users:
                if user.get('user_id') == 0:
                    return user.get('username')
        
        # Fallback if no user 0 found
        return os.getenv('USERNAME', 'User')
    except Exception as e:
        print(f"Error getting default username: {e}")
        return os.getenv('USERNAME', 'User')


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
        self.username = get_default_username()
        self.session_file = f"{self.username}/SESSION_{self.username}.json"

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
            "username": self.username,
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

    def delete_session(self, start_timestamp):
        """
        Delete a session by start_timestamp from the session file.
        """
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

            # Remove the session with matching start_timestamp
            original_length = len(existing_data)
            existing_data = [
                session for session in existing_data 
                if session.get("start_timestamp") != start_timestamp
            ]

            # Only update S3 if something was actually deleted
            if len(existing_data) < original_length:
                self.client.put_object(
                    Bucket=self.bucket_name,
                    Key=self.session_file,
                    Body=json.dumps(existing_data),
                    ContentType="application/json",
                )
                return True
            else:
                return False

        except Exception as e:
            print(f"Error deleting session: {e}")
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

    def update_media_metadata(self, s3_key, metadata):
        """
        Update metadata for a specific media file using S3 Object Tags.
        Tags allow metadata to be stored without modifying the object's LastModified timestamp.
        
        Args:
            s3_key: The S3 key of the media file (e.g., "username/session123/video_timestamp.mp4")
            metadata: Dict of metadata to update (e.g., {"app_name": "Discord"})
        """
        try:
            # Get existing tags for this object
            try:
                response = self.client.get_object_tagging(Bucket=self.bucket_name, Key=s3_key)
                existing_tags = {tag['Key']: tag['Value'] for tag in response.get('TagSet', [])}
            except self.client.exceptions.NoSuchKey:
                existing_tags = {}
            
            # Update with new metadata
            updated_tags = {**existing_tags, **metadata}
            
            # Convert to TagSet format for put_object_tagging
            tag_set = [{'Key': k, 'Value': str(v)} for k, v in updated_tags.items()]
            
            # Update object tags (does not modify LastModified)
            self.client.put_object_tagging(
                Bucket=self.bucket_name,
                Key=s3_key,
                Tagging={'TagSet': tag_set}
            )
            return True
        except Exception as e:
            print(f"Error updating media metadata: {e}")
            return False
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
