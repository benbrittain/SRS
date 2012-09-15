import os, json
from flask import Flask, render_template, redirect, url_for, request
from flask.ext.assets import Environment, Bundle
from flask.ext.login import (LoginManager, current_user, login_required,
    login_user, logout_user, UserMixin, AnonymousUser, flash,
    confirm_login, fresh_login_required)
from LoginForm import LoginForm, RegistrationForm
from mongo import User

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
    user = User.query.get(user_id)
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
    user = User.query.filter(User.username == unicode(form.username.data), User.password == unicode(form.password.data)).first()
    if user:
        if login_user(DbUser(user)):
            ustring = '['
            for x in user.decks:
                ustring = ustring +  "{name:\"" + x.name.encode('utf8') + "\"}"
            ustring = ustring + ']'
            return render_template('index.html', decks = json.JSONEncoder(ustring))
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
    return render_template('index.html', decks = current_user)


#run everything! move into an __init__.py?
if __name__ == '__main__':
  app.run()
