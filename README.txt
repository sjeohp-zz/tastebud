
./run.py

./runp.py
	
./manage.py db upgrade
./manage.py db migrate

flask/bin/python
from app import db, models
users = models.User.query.all()	