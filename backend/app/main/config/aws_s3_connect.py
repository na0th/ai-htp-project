import boto3
import botocore

bucket_name = 'ai-htp-test'

s3 = boto3.resource('s3') 

for bucket in s3.buckets.all(): 
	print(bucket.name)
 
