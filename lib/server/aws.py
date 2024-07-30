import boto3
import io
from lib.globals import USERNAME

class S3:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        self.bucket_name = "my-local-bucket"

    def bucket_exists(self):
        # Check if a bucket exists
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
            # Create a bucket
            self.client.create_bucket(Bucket=self.bucket_name)

    def get(self):
        return self

    def upload(self, fileName):
        remote_fileName = fileName + USERNAME
        self.client.upload_file(fileName, 'my-local-bucket', remote_fileName)
        #need to append user to the remote file name at some point
        #probably need to manually build different versions for every user

    def list(self):
        # List buckets
        response = self.client.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def download(self, object_name):
        # Download a file from S3 into memory
        remote_objectName = object_name+USERNAME
        response = self.client.get_object(Bucket=self.bucket_name, Key=remote_objectName)
        file_content = response['Body'].read()
        return io.BytesIO(file_content)
