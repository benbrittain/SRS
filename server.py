import os, json
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask.ext.assets import Environment, Bundle
from flask.ext.login import (LoginManager, current_user, login_required,
    login_user, logout_user, UserMixin, AnonymousUser, flash,
    confirm_login, fresh_login_required)
from LoginForm import LoginForm, RegistrationForm
from mongo import User, Deck
from json import JSONEncoder


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
        query = User(username = request.form['username'], password = request.form['password'], decks = [])
        query.save()
        return render_template('index.html')
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

#merged with below?
@app.route('/decks/<deckName>/edit')
@login_required
def edit_deck(deckName):
    pass

@app.route('/decks/<deckName>')
@login_required
def show_deck(deckName):
    pass

@app.route('/decks')
@app.route('/')
@login_required
def decks_index():
    user = User.query.filter(User.username == current_user.get_id()).first()
    decks = map(lambda deck: {'name': deck.name, 'cards': deck.cards}, user.decks)
    ustring = '['
    for card in decks:
        if len(card['cards'])> 0:
            cardSides = "{front: \" " + card['cards'][0].front.encode('utf8') + " \", back: \" " + card['cards'][0].back.encode('utf8') + " \" }"
        else:
            cardSides = "{}"
        ustring = ustring +  "{name:\"" + card['name'].encode('utf8') + "\", cards: " + cardSides +" }"
    ustring = ustring + ']'
        
    
    return render_template('index.html', decks=json.dumps(ustring))

@app.route('/decks', methods=['POST'])
@login_required
def decks_create():
    print request.json
    user = User.query.filter(User.username == request.json['username']).first()
    deck = Deck(name=request.json['name'], cards=[])
    user.decks.append(deck)
    if user.save():
        return jsonify(name=deck.name, cards=[])
    else:
        return jsonify(success=False)

#run everything! move into an __init__.py?
if __name__ == '__main__':
    app.run()
