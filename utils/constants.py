import nltk
import string

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