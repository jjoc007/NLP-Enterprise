from processor import *
import os
import textract
import unidecode
import hashlib
import magic
from datetime import datetime
from consolidate import *
import re

for fn in os.listdir(LOCATION_FILES + "files/"):
    if magic.from_file(LOCATION_FILES + "files/" + fn, mime=True) in MIME_VALID.keys():
        try:
            file_name_md5 = hashlib.md5(fn.encode('utf-8')).hexdigest()
            mime_type = magic.from_file(LOCATION_FILES + "files/" + fn, mime=True)
            ext = MIME_VALID.get(mime_type)
            text = unidecode.unidecode(
                str(textract.process(LOCATION_FILES + "files/" + fn, extension=ext).decode('utf8')))

            text = re.sub('\W+', ' ', text.lower())
            process_text(fn, file_name_md5, text)

            # guardar en dynamo
            file_row = {
                "_id": file_name_md5,
                "extension": ext,
                "mime_type": mime_type,
                "origin": {
                    "type": "web_page",
                    "url": "https://www.udistrital.edu.co/"
                },
                "name": fn,
                "md5_name": file_name_md5,
                "date_extraction": datetime.now(),
                "location_s3": ""
            }

            mongo_saver.save_file_metadata(file_row)

        except:
            print("Error Procesando archivo")


# consolidar palabras mas frecuentes y guardarlas en diccionario
consolidate()
