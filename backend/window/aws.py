import boto3
from globals import USERNAME
import requests
import os
import json
from datetime import datetime

ARN = 'arn:aws:iam::378382627972:role/digitaldiary-devteam'
localhost = 'http://127.0.0.1:5000/'


class S3:
    def __init__(self):
        print("this is correct")
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
                'timestamp': datetime.now().isoformat(),
                'end_time': None  # Initialize with no end time
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

    def end_session(self, game_id=None):
        """End the current session by adding an end time"""
        try:
            # Try to read existing file
            try:
                response = self.client.get_object(
                    Bucket=self.bucket_name,
                    Key=self.session_file
                )
                existing_data = json.loads(response['Body'].read().decode('utf-8'))
                if not isinstance(existing_data, list):
                    return False
            except self.client.exceptions.NoSuchKey:
                # File doesn't exist
                return False

            # Find the most recent session without an end_time
            session_to_end = None
            session_index = None
            
            for i in range(len(existing_data) - 1, -1, -1):  # Iterate backwards
                session = existing_data[i]
                # Check if session doesn't have end_time or end_time is None
                if session.get('end_time') is None:
                    # If game_id is specified, make sure it matches
                    if game_id is None or session.get('game_id') == game_id:
                        session_to_end = session
                        session_index = i
                        break

            if session_to_end is None:
                print("No active session found to end")
                return False

            # Add end time to the session
            existing_data[session_index]['end_time'] = datetime.now().isoformat()

            # Upload updated file
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=self.session_file,
                Body=json.dumps(existing_data),
                ContentType='application/json'
            )

            return True
        except Exception as e:
            print(f"Error ending session: {str(e)}")
            return False

    def get_latest_session(self):
        """Get the most recent session entry from the JSON file"""
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.session_file
            )
            session_data = json.loads(response['Body'].read().decode('utf-8'))
            print(response)
            print(session_data)
            if not session_data:
                return None

            # Return the most recent entry (last in the list)
            latest_session = session_data[-1]
            
            # Handle backward compatibility - sessions might not have end_time field
            if 'end_time' not in latest_session:
                latest_session['end_time'] = None
                
            return latest_session
        except self.client.exceptions.NoSuchKey:
            # File doesn't exist
            return None
        except Exception as e:
            print(f"Error getting latest session: {str(e)}")
            return None

    def get_active_session(self):
        """Get the most recent session that hasn't ended yet"""
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.session_file
            )
            session_data = json.loads(response['Body'].read().decode('utf-8'))
            
            if not session_data:
                return None

            # Find the most recent session without an end_time
            for i in range(len(session_data) - 1, -1, -1):  # Iterate backwards
                session = session_data[i]
                # Handle backward compatibility
                if 'end_time' not in session:
                    session['end_time'] = None
                
                if session['end_time'] is None:
                    return session
                    
            return None  # No active session found
        except self.client.exceptions.NoSuchKey:
            # File doesn't exist
            return None
        except Exception as e:
            print(f"Error getting active session: {str(e)}")
            return None

    def get_all_sessions_with_durations(self):
        """Get all sessions with calculated durations"""
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.session_file
            )
            session_data = json.loads(response['Body'].read().decode('utf-8'))
            
            if not session_data:
                return []

            sessions_with_durations = []
            
            for i, session in enumerate(session_data):
                # Handle backward compatibility
                if 'end_time' not in session:
                    session['end_time'] = None
                
                # Parse start time
                start_time = datetime.fromisoformat(session['timestamp'])
                
                # Calculate end time and duration
                if session['end_time'] is not None:
                    # Session has an explicit end time
                    end_time = datetime.fromisoformat(session['end_time'])
                    duration_seconds = (end_time - start_time).total_seconds()
                else:
                    # Session doesn't have an end time, calculate based on rules
                    two_hours_seconds = 2 * 60 * 60  # 2 hours in seconds
                    
                    if i + 1 < len(session_data):
                        # There's a next session, calculate time to next session
                        next_session_start = datetime.fromisoformat(session_data[i + 1]['timestamp'])
                        time_to_next_seconds = (next_session_start - start_time).total_seconds()
                        
                        # Use the smaller of 2 hours or time to next session
                        duration_seconds = min(two_hours_seconds, time_to_next_seconds)
                    else:
                        # This is the last session, use 2 hours
                        duration_seconds = two_hours_seconds
                
                # Create session with duration info
                session_with_duration = {
                    'game_id': session['game_id'],
                    'start_time': session['timestamp'],
                    'end_time': session['end_time'],
                    'duration_seconds': duration_seconds,
                    'duration_minutes': round(duration_seconds / 60, 2),
                    'duration_hours': round(duration_seconds / 3600, 2)
                }
                
                sessions_with_durations.append(session_with_duration)
            
            return sessions_with_durations
            
        except self.client.exceptions.NoSuchKey:
            # File doesn't exist
            return []
        except Exception as e:
            print(f"Error getting sessions with durations: {str(e)}")
            return []