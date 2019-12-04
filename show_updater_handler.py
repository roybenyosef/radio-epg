import os
import json
import boto3
from botocore.exceptions import ClientError

S3 = boto3.client('s3')


def main(event, context):
    try:
        response = S3.get_object(Bucket=os.environ['DATA_BUCKET_NAME'], Key='epg_data.json')
        file_content = json.loads(response['Body'].read())
        print(f'File content: {file_content}')

        out_data = file_content[0]['epg']['Sun'][0]
        S3.put_object(Body=out_data, Bucket=os.environ['OUT_BUCKET_NAME'], Key='epg.json')

    except ClientError as e:
        raise
