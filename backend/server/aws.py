import boto3
import io
from backend.globals import USERNAME
import requests
import os
import json
from datetime import datetime

ARN = 'arn:aws:iam::378382627972:role/digitaldiary-devteam'
localhost = 'http://127.0.0.1:5000/'


class S3:
    def __init__(self):
        sts_client = boto3.client('sts')
        assumed_role = sts_client.assume_role(
            RoleArn=ARN,
            RoleSessionName="SessionName"
        )
        credentials = assumed_role['Credentials']

        # Use the temporary credentials to create the S3 client
        self.client = boto3.client(
            's3',
            region_name='us-west-2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        self.bucket_name = "digital-diary"
        self.session_file = f"SESSION_{USERNAME}.json"

    def bucket_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            return True
        except self.client.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                return False
            else:
                raise

    def create(self):
        if self.bucket_exists():
            print("The bucket already exists:", self.bucket_name)
        else:
            self.client.create_bucket(Bucket=self.bucket_name)

    def get(self):
        return self

    def get_presigned_url(self, file_path, game_id=None):
        localhost_url = localhost + 'generate-presigned-url'
        data = {
            'file_name': os.path.basename(file_path),
            'username': USERNAME
        }
        if game_id:
            data['game_id'] = game_id

        response = requests.post(
            localhost_url,
            json=data
        )
        response.raise_for_status()
        return response.json()['url']

    def update_session(self, game_id):
        """Add a new session entry to the JSON file"""
        try:
            # Create session data
            session_entry = {
                'game_id': game_id,
                'timestamp': datetime.now().isoformat()
            }

            # Try to read existing file
            try:
                response = self.client.get_object(
                    Bucket=self.bucket_name,
                    Key=self.session_file
                )
                existing_data = json.loads(response['Body'].read().decode('utf-8'))
                if not isinstance(existing_data, list):
                    existing_data = []
            except self.client.exceptions.NoSuchKey:
                # File doesn't exist, create new list
                existing_data = []

            # Append new entry
            existing_data.append(session_entry)

            # Upload updated file
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=self.session_file,
                Body=json.dumps(existing_data),
                ContentType='application/json'
            )

            return True
        except Exception as e:
            print(f"Error updating session: {str(e)}")
            return False

    def get_latest_session(self):
        """Get the most recent session entry from the JSON file"""
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.session_file
            )
            session_data = json.loads(response['Body'].read().decode('utf-8'))

            if not session_data:
                return None

            # Return the most recent entry (last in the list)
            return session_data[-1]
        except self.client.exceptions.NoSuchKey:
            # File doesn't exist
            return None
        except Exception as e:
            print(f"Error getting latest session: {str(e)}")
            return None