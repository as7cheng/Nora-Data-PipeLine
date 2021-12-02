"""
File to get and update info for the file hold in S3 bucket
"""
import json
import boto3
from botocore.exceptions import ClientError


S3 = boto3.client('s3')
BUCKET = 'nora-data-log'
KEY = 'offset.json'


def handle_offset() -> int:
    """
    Function to get and update offset stored in the file hold
    in the S3 bucket
    """
    data = download_file(BUCKET, KEY)
    offset = get_offset(data)
    print('Before modification', offset)
    data['offset'] = offset + 1
    update_file(data)
    new_data = download_file(BUCKET, KEY)
    new_offset = get_offset(new_data)
    print('After modification', new_offset)
    return offset


def download_file(bucket, key) -> dict:
    """
    Helper function to download the file data from the S3 bucket
    """
    try:
        resource = S3.get_object(Bucket=bucket, Key=key)
        data = resource['Body'].read().decode('utf-8')
        data = json.loads(data)
        return data
    except ClientError as error:
        print(error)


def get_offset(data) -> int:
    """
    Helper function to read offset from the file data
    """
    return data['offset'] if 'offset' in data else 0


def update_file(data) -> None:
    """
    Helper function to update offset from the file data
    """
    try:
        new_data = json.dumps(data)
        response = S3.put_object(Body=new_data.encode('utf-8'), Bucket=BUCKET, Key=KEY)
        print(response)
    except ClientError as error:
        print(error)
