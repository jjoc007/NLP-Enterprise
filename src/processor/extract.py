import src.s3.s3 as s3
from .processor import *
from src.neo4j.service.file import *
import textract
import unidecode
import hashlib
from datetime import datetime
import scipy
import magic
import re

from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer('test111')

def process_2(bucket, item):
    s3.download_file(bucket, item)
    data = pd.read_csv("/tmp/" + item)
    corpus = data.Texto.tolist()
    textos = data.Texto.tolist()

    corpus_embeddings = embedder.encode(corpus)
    embedder.save("test111")

    queries = ['nacimiento universidad']
    query_embeddings = embedder.encode(queries)

    number_top_matches = 5

    for query, query_embedding in zip(queries, query_embeddings):
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 3 most similar sentences in corpus:")

        for idx, distance in results[0:number_top_matches]:
            print(textos[idx].strip(),
                  "(Index: %s " % idx)


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

