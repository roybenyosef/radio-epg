import os
import json
import boto3
from botocore.exceptions import ClientError

S3 = boto3.client('s3')


def main(event, context):
    try:
        response = S3.get_object(Bucket=os.environ['BUCKET_NAME'], Key='epg_data.json')
        file_content = json.loads(response['Body'].read())
        print(f'File content: {file_content}')
    except ClientError as e:
        raise
