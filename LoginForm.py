from flask.ext.wtf import Form, TextField, PasswordField, validators
from mongo import *

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

