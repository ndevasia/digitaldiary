"""
S3-based API usage logging for tracking feature usage.
Stores logs in S3 with one file per user (e.g., username/logs.json)
"""

import json
import os
import boto3
from datetime import datetime
from functools import wraps
from flask import request

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "digital-diary")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


class S3UsageLogger:
    """Logs API usage to S3 for each user."""
    
    def __init__(self):
        self.bucket = AWS_S3_BUCKET
        self.region = AWS_REGION
        try:
            self.s3_client = boto3.client(
                "s3",
                region_name=self.region,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
            self.available = True
        except Exception as e:
            print(f"Warning: Could not initialize S3 client for logging: {e}")
            self.available = False
    
    def log_api_call(self, username, feature_name, endpoint, method, status_code, response_time_ms, page_source=None):
        """
        Log an API call to the user's logs file in S3.
        
        Args:
            username: Username making the call
            feature_name: Human-readable feature name (e.g., "screenshot_capture")
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            status_code: HTTP response status code
            response_time_ms: Time taken in milliseconds
            page_source: Optional page/component name making the request (e.g., "FilesPage", "ScrapbookEditorPage")
        """
        if not self.available:
            return
        
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "feature": feature_name,
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "response_time_ms": round(response_time_ms, 2),
            }
            
            # Add page source if provided
            if page_source:
                log_entry["page_source"] = page_source
            
            logs_key = f"{username}/logs.json"
            
            # Try to read existing logs
            existing_logs = []
            try:
                response = self.s3_client.get_object(Bucket=self.bucket, Key=logs_key)
                content = response['Body'].read().decode('utf-8')
                existing_logs = json.loads(content)
            except self.s3_client.exceptions.NoSuchKey:
                # File doesn't exist yet, start fresh
                existing_logs = []
            except Exception as e:
                print(f"Warning: Could not read existing logs for {username}: {e}")
                existing_logs = []
            
            # Append new log entry
            existing_logs.append(log_entry)
            
            # Write back to S3
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=logs_key,
                Body=json.dumps(existing_logs, indent=2),
                ContentType="application/json"
            )
        
        except Exception as e:
            print(f"Error logging API call for {username}: {e}")
    
    def log_error(self, username, feature_name, endpoint, method, error_message, page_source=None):
        """Log an error API call."""
        if not self.available:
            return
        
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "feature": feature_name,
                "endpoint": endpoint,
                "method": method,
                "error": error_message,
                "status": "error",
            }
            
            # Add page source if provided
            if page_source:
                log_entry["page_source"] = page_source
            
            logs_key = f"{username}/logs.json"
            
            # Try to read existing logs
            existing_logs = []
            try:
                response = self.s3_client.get_object(Bucket=self.bucket, Key=logs_key)
                content = response['Body'].read().decode('utf-8')
                existing_logs = json.loads(content)
            except self.s3_client.exceptions.NoSuchKey:
                existing_logs = []
            except Exception as e:
                print(f"Warning: Could not read existing logs for {username}: {e}")
                existing_logs = []
            
            # Append error entry
            existing_logs.append(log_entry)
            
            # Write back to S3
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=logs_key,
                Body=json.dumps(existing_logs, indent=2),
                ContentType="application/json"
            )
        
        except Exception as e:
            print(f"Error logging error for {username}: {e}")


# Initialize global logger
usage_logger = S3UsageLogger()


def log_usage(feature_name=None):
    """
    Decorator to log API endpoint usage to S3.
    
    Usage:
        @app.route('/api/<username>/screenshot', methods=['POST'])
        @log_usage(feature_name="screenshot_capture")
        def upload_screenshot(username):
            ...
    
    Args:
        feature_name: Descriptive name for the feature being logged
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = request.headers.get('X-Username', 'unknown')
            endpoint = request.path
            method = request.method
            page_source = request.headers.get('X-Page-Source', None)
            start_time = datetime.utcnow()
            
            try:
                result = func(*args, **kwargs)
                
                # Extract status code from response
                if isinstance(result, tuple):
                    status_code = result[1] if len(result) > 1 else 200
                else:
                    status_code = 200
                
                # Calculate response time
                response_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Log to S3
                usage_logger.log_api_call(
                    username=username,
                    feature_name=feature_name or func.__name__,
                    endpoint=endpoint,
                    method=method,
                    status_code=status_code,
                    response_time_ms=response_time_ms,
                    page_source=page_source
                )
                
                return result
            
            except Exception as e:
                # Calculate response time even for errors
                response_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Log error to S3
                usage_logger.log_error(
                    username=username,
                    feature_name=feature_name or func.__name__,
                    endpoint=endpoint,
                    method=method,
                    error_message=str(e),
                    page_source=page_source
                    endpoint=endpoint,
                    method=method,
                    error_message=str(e)
                )
                raise
        
        return wrapper
    return decorator
