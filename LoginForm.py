from flask.ext.wtf import Form, TextField, PasswordField, validators
from mongo import *

class RegistrationForm(Form):
    username = TextField('username', [validators.Required()])
    password = TextField('password', [validators.Required()])
    confirm_password = TextField('confirm_password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        dbUser = User.query.filter(User.username == unicode(self.username.data)).first()
        print(dbUser)
        u
        if dbUser:
            flash('username is already taken')
            return False
        if (self.password.data != self.confirm_password.data):
            flash('Passwords do not match!')
            return False
        query = User(username = self.username.data, password = self.password.data, decks = [])
        query.save()
        return False 

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
#        if not rv:
#            return False
        dbUser = User.query.filter(User.username == unicode(self.username.data), User.password == unicode(self.password.data)).first()
        warn(dbUser)
        if dbUser:
            #make this HASHING IN THE FUTURE MAN! `
            if unicode(self.username.data) == unicode(dbUser.username):
                if unicode(self.password.data) == unicode(dbUser.password):
                    return True
        return False 

