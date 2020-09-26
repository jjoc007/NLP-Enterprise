import boto3
from botocore.exceptions import ClientError
import os
import glob

s3 = boto3.resource('s3')


def download_file(bucket, item):
    try:
        s3.Bucket(bucket).download_file(item, "/tmp/" + item)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def upload_file(file_name, bucket, item):
    try:
        s3.meta.client.upload_file(file_name, bucket, item)
    except ClientError as e:
        raise


def clean_files():
    files = glob.glob('/tmp/corpus/*')
    for f in files:
        os.remove(f)

    files = glob.glob('/tmp/nlp_tmp_files/*')
    for f in files:
        os.remove(f)
