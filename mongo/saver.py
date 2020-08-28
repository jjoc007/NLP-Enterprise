from .config import nlp_db


def save_file_metadata(data):
    file_metadata_collection = nlp_db["file_metadata"]
    x = file_metadata_collection.insert_one(data)


def save_file_dictionary(data):
    file_dictionary_collection = nlp_db["file_dictionary"]
    x = file_dictionary_collection.insert_one(data)


def get_all_file_dictionary():
    company_dictionary_collection = nlp_db["file_dictionary"]
    return list(company_dictionary_collection.find({}))


def save_company_dictionaries(list_data):
    company_dictionary_collection = nlp_db["company_dictionary"]
    company_dictionary_collection.insert(list_data)


def save_company_dictionary(data):
    company_dictionary_collection = nlp_db["company_dictionary"]
    company_dictionary_collection.replaceOne(data)




