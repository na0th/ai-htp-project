import boto3
import os

s3 = boto3.client('s3',
    		aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
            	aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'))
bucket_name = 'ai-htp-test'

response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    print(f"Bucket: {bucket_name}")
    print("Files:")
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print(f"No files found in the bucket: {bucket_name}")
