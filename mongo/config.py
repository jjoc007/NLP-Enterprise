import pymongo

nlp_client = pymongo.MongoClient("mongodb://mongoadmin:secret@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false")
nlp_db = nlp_client["nlp"]
