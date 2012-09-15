import os
from flask import Flask, render_template, redirect
from flask.ext.assets import Environment, Bundle
from flask.ext.login import (LoginManager, current_user, login_required,
    login_user, logout_user, UserMixin, AnonymousUser, flash,
    confirm_login, fresh_login_required)
from LoginForm import LoginForm
from mongo import User

app = Flask(__name__)

# Debugging
app.debug = (os.environ.get('ENV', 'production') != True)
app.secret_key= "why do I feel awake at 4am?"
app.config.from_object(__name__)

#login Manager setup

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

 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter(User.username == unicode(form.username.data), User.password == unicode(form.password.data)).first()
    if user:
        if login_user(DbUser(user)):
            flash("You have logged in")
            return render_template('layout.html')
    return render_template('login.html')


@app.route('/')
@app.route('/decks')
def decks_index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run()
