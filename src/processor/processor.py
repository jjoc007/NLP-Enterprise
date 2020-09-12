import sys
import texthero as hero
from src.utils.constants import *
import src.dynamo.file_dictionary as file_dictionary


def process_text(real_name, file_name_md5, text_input):

    text_input = replace_entities(text_input)

    dataDict = {
        'text': [text_input]
    }
    df = pd.DataFrame(dataDict)

    df['clean_data'] = hero.clean(df['text'], pipeline=custom_pipeline)
    df['clean_data'] = hero.remove_stopwords(df['clean_data'], stopwords)
    top_words = hero.visualization.top_words(df['clean_data'])

    clean_top_words = clean_tokens_words(top_words)
    #n = clean_top_words.head(40).plot.bar(rot=90, title="Top 40 words of "+real_name)
    #n.get_figure().savefig(file_name_md5+'_plot.jpg', format='jpg', bbox_inches="tight")

    y = hero.wordcloud(df['clean_data'], max_words=40, return_figure=True)
    y.savefig(file_name_md5+'_cloud_word.jpg', format='jpg')

    words = []
    if len(clean_top_words.keys()) > 0:
        for word in clean_top_words.keys():
            words.append({
                "word": word.replace("-", " "),
                "frequency": int(top_words.get(key=word))
            })

    data = {
        "file_id": file_name_md5,
        "word_frequency": words
    }

    file_dictionary.put_file_dictionary(data)



def clean_tokens_words(top_words):
    words = []

    for key in top_words.keys():
        if len(key) < 3:
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
