import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.script import Manager
# from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS
# import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

from app import app, db
app.config.from_object('config')

# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models