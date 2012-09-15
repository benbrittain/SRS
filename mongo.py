from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy, BaseQuery
app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'library'
db = MongoAlchemy(app)

class Card(db.Document):
    #stores whats on the card. May be abstracted further out
    front = db.StringField()
    back = db.StringField()

    #used for calculating the SRS numbers
    interval = db.IntField()
    eFactor = db.FloatField()

class Deck(db.Document):
    name = db.StringField()
    userId = db.StringField()
    cards = db.ListField(db.DocumentField('Card'))

class User(db.Document):
    username = db.StringField()
    password = db.StringField()
    decks = db.ListField(db.DocumentField('Deck'))
