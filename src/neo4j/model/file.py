import src.neo4j.model.word as word
import src.neo4j.model.word_per_file as word_per_file
from neomodel import (StructuredNode, StringProperty, UniqueIdProperty, RelationshipTo)


class File(StructuredNode):
    uid = UniqueIdProperty(primary=True)
    name = StringProperty(required=True)
    url = StringProperty(required=True)

    has_words = RelationshipTo(word.Word, "HAS", model=word_per_file.WordPerFile)

    def parse(self, json_data):
        self.uid = json_data["uid"]
        self.name = json_data["name"]
        self.url = json_data["url"]

    def to_json(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "url": self.url,
        }