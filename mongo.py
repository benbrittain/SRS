from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy, BaseQuery
app = Flask(__name__)

app.config['MONGOALCHEMY_DATABASE'] = 'library'
db = MongoAlchemy(app)

class MyCustomizedQuery(BaseQuery):
    def check_exists(self, name):
        return self.filter(self.type.username == name).first()

#class Card(db.Document):
#    front = db.StringField()
#    back = db.StringField()
#
#class Deck(db.Document):
#    name = db.StringField()
#    cards = db.DocumentField(Card)

class User(db.Document):
    username = db.StringField()
    password = db.StringField()
#    decks = db.ListField(db.DocumentField(Deck))

    query_class = MyCustomizedQuery
#    decks = db.DocumentField(Deck)

