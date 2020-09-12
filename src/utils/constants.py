import nltk
import string
import pandas as pd
from texthero import preprocessing

pd.options.display.max_colwidth = 100
pd.set_option("display.max_rows", 999)
NUM_TOP_WORDS = 20

custom_pipeline = [preprocessing.fillna,
                   preprocessing.lowercase,
                   preprocessing.remove_digits,
                   preprocessing.remove_punctuation,
                   preprocessing.remove_diacritics,
                   preprocessing.remove_stopwords,
                   preprocessing.remove_whitespace,
                   preprocessing.remove_urls
                   ]

string.punctuation = r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""

LOCATION_FILES = '/home/juan/Documentos/files_nlp_process/'
MIME_VALID = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.oasis.opendocument.text": "odt",
    "application/msword": "doc",
    "text/plain": "txt",
    "application/pdf": "pdf",
    "image/png": "png"
}

S3_BUCKET_FILES = 'nlp-company'

stopwords = nltk.corpus.stopwords.words('spanish')
stopwords.extend(['texto',
                  'textos',
                  'cada',
                  'dos',
                  'edu',
                  'anos',
                  'ser',
                  'segun',
                  'horas',
                  'caso',
                  'puede',
                  'segun',
                  'retiro',
                  'mas',
                  'sido',
                  '10deg',
                  'piso',
                  'debe',
                  'mediante',
                  'llwww',
                  'general',
                  'agosto',
                  'cargo',
                  'dias',
                  'tiempo',
                  'pagina',
                  'funciones'])