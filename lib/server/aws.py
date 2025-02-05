import boto3
import io
from lib.globals import USERNAME
import requests
import os

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
    
    def get_presigned_url(self, file_path):
        localhost_url = localhost + 'generate-presigned-url'
        response = requests.post(

            'http://127.0.0.1:5000/generate-presigned-url',
            localhost_url,
            json={'file_name': os.path.basename(file_path), 'username': USERNAME}
        )
        response.raise_for_status()
        return response.json()['url']
