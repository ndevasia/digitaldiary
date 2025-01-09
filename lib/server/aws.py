import boto3
import io
from lib.globals import USERNAME

class S3:
    def __init__(self):
        self.client = boto3.client(
            's3',
            region_name='us-west-2'
        )
        self.bucket_name = "digital-diary"

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
        self.client.upload_file(fileName, self.bucket_name, remote_fileName)
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
