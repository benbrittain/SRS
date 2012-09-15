import os
from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle
from flask.ext.login import (LoginManager, current_user, login_required,
    login_user, logout_user, UserMixin, AnonymousUser,
    confirm_login, fresh_login_required)
from LoginForm import LoginForm

app = Flask(__name__)
app.secret_key= "why do I feel awake at 4am?"


#TEMPORARY FOR TESTING
class User(UserMixin):
    def __init__(self, name, password, active=True):
        self.name = name
        self.password = password 
        self.active = active

    def is_active(self):
        return self.active

 
USERS = {
    1: User(u"Ben", "Haskell"),
    2: User(u"David", "Ruby")
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

 

# Debugging
app.debug = (os.environ.get('ENV', 'production') != True)

# Login
def load_user(userid):
    return User.get(userid)

# Routing
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.username)
        session['user_id'] = form.user.id
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/')
@app.route('/decks')
def decks_index():
    return render_template('index.html')

if __name__ == '__main__':
  app.run()
