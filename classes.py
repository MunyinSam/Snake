from mongoengine import Document, fields, connect, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentListField
from dotenv import load_dotenv
import os

load_dotenv()

connect('SnakeGame', host=str(os.getenv("MONGODB_URI")))

class Player(Document):
    name = fields.StringField()
    position = fields.IntField()

class Tile(EmbeddedDocument):
    type = StringField(choices=["normal","up","down"])
    occupied_by = ListField(StringField())

class Board(Document):
    board_name = StringField()
    players = ListField(StringField())
    tiles = EmbeddedDocumentListField(Tile)
    state = StringField()
    current_turn = StringField()