from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, PasswordField, HiddenField
from wtforms.validators import Required, Length
from app.models import User

class CreateForm(Form):
	nickname = TextField('nickname', validators = [Required()])
	email = TextField('email', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	confirmation = PasswordField('confirmation', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class LoginForm(Form):
	email = TextField('email', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class OpenIDForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default=False)

class GroupForm(Form):
    group_name = TextField('group_name', validators = [Required()])
    
class TagForm(Form):
    tag_body = TextField('tag_body', validators = [Required()])
    group_name = HiddenField('group_name')
	
class SearchForm(Form):
	search = TextField('search', validators = [Required()])