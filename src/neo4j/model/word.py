from neomodel import (StructuredNode, IntegerProperty, UniqueIdProperty)


class Word(StructuredNode):
    word = UniqueIdProperty(primary=True)
    frequency = IntegerProperty(required=True)

    def parse(self, json_data):
        self.word = json_data["word"]
        self.frequency = json_data["frequency"]

    def to_json(self):
        return {
            "word": self.word,
            "frequency": self.frequency,
        }