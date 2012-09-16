from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy, BaseQuery
app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'library'
db = MongoAlchemy(app)

class Card(db.Document):
    #stores whats on the card. May be abstracted further out
    front = db.StringField()
    back = db.StringField()

    uniqueId = db.StringField()
    #used for calculating the SRS numbers

    repetition = db.IntField()
    interval = db.IntField()
    lastDone = db.DateTimeField()
    eFactor = db.FloatField()
    status = db.StringField()
    isDue = db.BoolField()


class Deck(db.Document):
    name = db.StringField()
    userId = db.StringField()
    cards = db.ListField(db.DocumentField('Card'))

class User(db.Document):
    username = db.StringField()
    password = db.StringField()
    decks = db.ListField(db.DocumentField('Deck'))
