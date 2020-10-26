import src.s3.s3 as s3
from .processor import *
from src.neo4j.service.file import *
import textract
import unidecode
import hashlib
from datetime import datetime


import magic
import re


def process(bucket, item):
    s3.download_file(bucket, item)
    if magic.from_file("/tmp/" + item, mime=True) in MIME_VALID.keys():

        file_name_md5 = hashlib.md5(item.encode('utf-8')).hexdigest()
        mime_type = magic.from_file("/tmp/" + item, mime=True)
        ext = MIME_VALID.get(mime_type)
        text = unidecode.unidecode(
            str(textract.process("/tmp/" + item, extension=ext).decode('utf8')))

        text = re.sub('\W+', ' ', text.lower())

        #guardar file
        file_json = {
            "uid" : file_name_md5,
            "name": item,
            "url": "https://www.udistrital.edu.co/"
        }

        file_object = save_file(file_json)

        process_text(item, file_object, text)

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

        s3.clean_files()

    return {'result': "Success"}

