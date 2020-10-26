from src.neo4j.model.word import Word


def save_word(word_json_object, file_object):
    word_object = search_word_by_id(word_json_object["word"])
    if word_object is None:
        word_object = Word()
        word_object.parse(word_json_object)
    else:
        word_object.frequency = word_object.frequency + word_json_object["frequency"]

    word_object.save()
    word_object.refresh()
    file_object.has_words.connect(word_object, {"frequency": word_json_object["frequency"]})

    return word_json_object


def search_word_by_id(word_id):
    return Word.nodes.get_or_none(word=word_id)