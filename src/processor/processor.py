import src.s3.s3 as s3
import texthero as hero
from src.utils.constants import *
from src.neo4j.service.word import *


def process_text(real_name, file_object, text_input):
    text_input = replace_entities(text_input)
    dataDict = {
        'text': [text_input]
    }
    df = pd.DataFrame(dataDict)

    df['clean_data'] = hero.clean(df['text'], pipeline=custom_pipeline)
    df['clean_data'] = hero.remove_stopwords(df['clean_data'], stopwords)
    top_words = hero.visualization.top_words(df['clean_data'])

    clean_top_words = clean_tokens_words(top_words)
    save_plot(clean_top_words, real_name, file_object.uid)
    #save_cloud_word(df['clean_data'], file_name_md5)

    words = []
    if len(clean_top_words.keys()) > 0:
        for word in clean_top_words.keys()[0:40]:

            word_json = {
                "word": word.replace("-", " "),
                "frequency": int(top_words.get(key=word))
            }
            save_word(word_json, file_object)


def save_plot(clean_top_words, real_name, file_name_md5):
    n = clean_top_words.head(40).plot.bar(rot=90, title="Top 40 words of "+real_name)
    n.get_figure().savefig("/tmp/nlp_tmp_files/" + file_name_md5+'_plot.jpg', format='jpg', bbox_inches="tight")

    s3.upload_file("/tmp/nlp_tmp_files/" + file_name_md5+'_plot.jpg', "nlp-bucket-corpus", 'results/'+file_name_md5+ '_plot.jpg')


def save_cloud_word(clean_data, file_name_md5):
    y = hero.wordcloud(clean_data, max_words=40, return_figure=True)
    y.savefig("/tmp/nlp_tmp_files/" +file_name_md5+'_cloud_word.jpg', format='jpg')

    s3.upload_file("/tmp/nlp_tmp_files/" + file_name_md5 +'_cloud_word.jpg', "nlp-bucket-corpus", 'results/' + file_name_md5 +'_cloud_word.jpg')


def clean_tokens_words(top_words):
    words = []

    for key in top_words.keys():
        if len(key) <= 3:
            continue
        words.append((key, top_words.get(key=key)))

    return pd.DataFrame(words).set_index(0)[1]


def replace_entities(input):
    input = input.lower()
    #entidades
    input = input.replace("universidad distrital francisco jose de caldas",
                                            "universidad-distrital-francisco-jose-de-caldas")
    input = input.replace("consejo superior universitario",
                          "consejo-superior-universitario")

    #plurales
    input = input.replace("contratos", "contrato")
    input = input.replace("docentes", "docente")
    input = input.replace("estudiantes", "estudiante")
    input = input.replace("articulos", "articulo")
    input = input.replace("objetivos", "objetivo")
    input = input.replace("leyes", "ley")
    input = input.replace("procedimientos", "procedimiento")
    input = input.replace("academicas", "academica")
    input = input.replace("academicos", "academico")

    #sinonimos
    input = input.replace("academico", "academica")

    return input
