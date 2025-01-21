import boto3
import io
from lib.globals import USERNAME
import requests
import os

class S3:
    def __init__(self):
        # Credentials are automatically retrieved if the backend has an IAM Role
        self.client = boto3.client('s3', region_name='us-west-2')
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

    def upload(self, fileName):
        remote_fileName = fileName + USERNAME
        self.client.upload_file(fileName, self.bucket_name, remote_fileName)

    def list(self):
        response = self.client.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def download(self, object_name):
        remote_objectName = object_name + USERNAME
        response = self.client.get_object(Bucket=self.bucket_name, Key=remote_objectName)
        file_content = response['Body'].read()
        return io.BytesIO(file_content)
    
    def get_presigned_url(self, file_path):
        response = requests.post(
            'http://localhost:5000/generate-presigned-url',
            json={'file_name': os.path.basename(file_path), 'username': USERNAME}
        )
        response.raise_for_status()
        return response.json()['url']
