from .processor import *
from ..dynamo.file_metadata import *
import textract
import unidecode
import hashlib
from datetime import datetime
import boto3
import botocore
import magic
import re


def process(bucket, item):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket).download_file(item, "/tmp/" + item)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    if magic.from_file("/tmp/" + item, mime=True) in MIME_VALID.keys():

        file_name_md5 = hashlib.md5(item.encode('utf-8')).hexdigest()
        mime_type = magic.from_file("/tmp/" + item, mime=True)
        ext = MIME_VALID.get(mime_type)
        text = unidecode.unidecode(
            str(textract.process("/tmp/" + item, extension=ext).decode('utf8')))

        text = re.sub('\W+', ' ', text.lower())
        process_text(item, file_name_md5, text)

        # guardar en dynamo
        file_row = {
            "file_id": file_name_md5,
            "extension": ext,
            "mime_type": mime_type,
            "origin": {
                "type": "web_page",
                "url": "https://www.udistrital.edu.co/"
            },
            "name": item,
            "md5_name": file_name_md5,
            "date_extraction": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "bucket_s3": bucket,
            "item_s3":item
        }
        put_file_metadata(file_row)


    return {'result': "Success"}

