import spacy
nlp = spacy.load("es_core_news_md")
nlp.add_pipe(nlp.create_pipe('sentencizer'))  # updated
import src.s3.s3 as s3
import textract
import unidecode
import hashlib
from src.utils.constants import *


import magic
import re


def converter_file(bucket, item):
    s3.download_file(bucket, item)
    if magic.from_file("/tmp/" + item, mime=True) in MIME_VALID.keys():
        file_name_md5 = hashlib.md5(item.encode('utf-8')).hexdigest()
        mime_type = magic.from_file("/tmp/" + item, mime=True)
        ext = MIME_VALID.get(mime_type)
        text = unidecode.unidecode(
            str(textract.process("/tmp/" + item, extension=ext).decode('utf8')))

        #text = re.sub('\W+', ' ', text.lower())
        text = text.lower().replace('\n', ' ')
        doc = nlp(text)


        sentences = [sent.string.strip() for sent in doc.sents  if len(sent.string.strip()) > 0]

        df = pd.DataFrame({"Texto": sentences})
        df.to_csv("/tmp/csv/" + file_name_md5 + ".csv")
        s3.upload_file("/tmp/csv/" + file_name_md5 + '.csv', "nlp-bucket-corpus",
                       'csv/' + file_name_md5 + '.csv')

    return {'result': "Success"}
