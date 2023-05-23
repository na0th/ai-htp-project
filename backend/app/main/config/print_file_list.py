import boto3

s3 = boto3.client('s3')
bucket_name = 'ai-htp-test'

response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    print(f"Bucket: {bucket_name}")
    print("Files:")
    for obj in response['Contents']:
        print(obj['Key'])
else:
    print(f"No files found in the bucket: {bucket_name}")
