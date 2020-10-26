from src.neo4j.model.file import File


def save_file(file_json_object):

    file_object = File()
    file_object.parse(file_json_object)
    file_object.save()
    file_object.refresh()

    return file_object
