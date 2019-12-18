import os
import boto3
from botocore.exceptions import ClientError

S3 = boto3.resource('s3')
epg_file_name = 'epg_data.json'


def main(event, context):
    try:
        copy_source = {
            'Bucket': os.environ['DATA_BUCKET_NAME'],
            'Key': epg_file_name
        }

        target_bucket = S3.Bucket(os.environ['OUT_BUCKET_NAME']);
        target_bucket.copy(copy_source, Key=epg_file_name)

    except ClientError as e:
        raise

