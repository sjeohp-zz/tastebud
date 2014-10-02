from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length
from app.models import User

class CreateForm(Form):
	nickname = TextField('nickname', validators = [Required()])
	email = TextField('email', validators = [Required()])
	password = TextField('password', validators = [Required()])
	confirmation = TextField('confirmation', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class LoginForm(Form):
	email = TextField('email', validators = [Required()])
	password = TextField('password', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class OpenIDForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class TagForm(Form):
	tag = TextField('tag', validators = [Required()])
	
class SearchForm(Form):
	search = TextField('search', validators = [Required()])