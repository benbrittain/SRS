import os, json, time
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask.ext.assets import Environment, Bundle
from flask.ext.login import (LoginManager, current_user, login_required,
    login_user, logout_user, UserMixin, AnonymousUser, flash,
    confirm_login, fresh_login_required)
from LoginForm import LoginForm
from mongo import User, Deck, Card
from json import JSONEncoder
import uuid
import srs

app = Flask(__name__)

## Debugging
app.debug = (os.environ.get('ENV', 'production') != True)
app.secret_key= "why do I feel awake at 4am?"
app.config.from_object(__name__)

##login Manager setup
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"
login_manager.setup_app(app)

class DbUser(UserMixin):
    """Wraps User object for Flask-Login"""
    def __init__(self, user):
        self._user = user

    def get_id(self):
        return unicode(self._user.username)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.username == user_id).first()
    if user:
        return DbUser(user)
    else:
        return None

#################
# Routing stuff #
#################

@app.route('/decks/<deckName>/start', methods=['GET'])
def initSRS(deckName):
    user = User.query.filter(User.username == request.args.get('username')).first()
    for deck in user.decks:
        if (unicode(deck.userId) == unicode(deckName)):
            for card in deck.cards:
                #SRS
                return jsonify(id=card.uniqueId,front=card.front,back=card.back)
    return jsonify(success=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        check = User.query.filter(User.username == unicode(request.form['username'])).first()
        if check:
            flash("user already exists")
            return render_template('register.html')
        if request.form['password'] != request.form['confirm_password']:
            flash("passwords do not match")
            return render_template('register.html')
        user = User(username = request.form['username'], password = request.form['password'], decks = [])
        user.save()
        login_user(DbUser(user))
        return redirect('/')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next = request.args.get("next")
    user = User.query.filter(User.username == unicode(form.username.data), User.password == unicode(form.password.data)).first()
    if user:
        if login_user(DbUser(user)):
            return redirect("/")
    return render_template('login.html')


@app.route('/profile/settings')
@login_required
def show_settings(deckName):
    pass

@app.route('/profile/')
@login_required
def show_profile():
    pass

#@app.route('/decks/<deckName>/<cardName>/delete', methods=['POST'])
#@login_required
#def delete_card(cardName):
#    print request.json
#    user = User.query.filter(User.username == current_user.get_id()).first()
#    for deck in user.decks:
#        if (unicode(deck.userId) == unicode(deckName)):
#            for card in deck:
#                if (card.uniqueId = cardId):
#
#            deck.cards.append(Card(front=request.json['front'], back=request.json['back'],interval=3,eFactor=3.0))
#    return jsonify(success=True)

@app.route('/decks/<deckName>/cards', methods=['POST'])
@login_required
def create_card(deckName):
    print request.json
    user = User.query.filter(User.username == request.json['username']).first()
    for deck in user.decks:
        if (unicode(deck.userId) == unicode(deckName)):
            deck.cards.append(srs.makeCard(request.json['front'],request.json['back']))
            user.save()
    return jsonify(success=True)

@app.route('/decks')
@login_required
def decks_index():
    user = User.query.filter(User.username == current_user.get_id()).first()
    decks = map(lambda deck: {'id': deck.userId , "name": deck.name, 'cards': [{'id': card.uniqueId, 'front': card.front, 'back': card.back} for card in deck.cards]}, user.decks)
    return render_template('index.html', decks=json.dumps(decks))

@app.route('/')
def homepage():
    if current_user.is_authenticated():
        return redirect(url_for('decks_index'))
    else:
        return redirect(url_for('register'))

@app.route('/decks', methods=['POST'])
@login_required
def decks_create():
    user = User.query.filter(User.username == request.json['username']).first()
    deck = Deck(name=request.json['name'], userId=str(uuid.uuid1()), cards=[])
    user.decks.append(deck)
    user.save()
    return jsonify(name=deck.name, id=deck.userId, cards=[])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


#run everything! move into an __init__.py?
if __name__ == '__main__':
    app.run()
