from __future__ import division
from app import db
from hashlib import md5
from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import asc, desc, func


ROLE_USER = 0
ROLE_ADMIN = 1
  
class UserTagAssoc(db.Model):
    __tablename__ = 'user_tags'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    user = db.relationship('User', backref=backref('user_tags', cascade="all, save-update, merge, delete, delete-orphan"))
    tag = db.relationship('Tag', backref=backref('user_tags', cascade="all, save-update, merge, delete, delete-orphan"))
    timestamp = db.Column(db.DateTime())
    def __repr__(self):
        return '<UserTagAssoc %r | %r>' % (self.user.nickname, self.tag.body)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(160), unique=True)
    created_at = db.Column(db.DateTime)
    users = association_proxy('user_tags', 'user')

    def __repr__(self):
    	return '<Tag %r>' % (self.body)

    @staticmethod
    def find_or_create(body):
    	tag = db.session.query(Tag).filter(Tag.body == body).first()
    	if tag == None:
    		tag = Tag(body=body, created_at=datetime.utcnow())
    		db.session.add(tag)
    		db.session.commit()
    	return tag

    @staticmethod
    def find(body):
    	tag = db.session.query(Tag).filter(Tag.body == body).first()
    	return tag

    def search_related_tags(self):
    	return db.session.query(Tag, func.count(UserTagAssoc.tag_id)) \
    	.filter(UserTagAssoc.user_id.in_(db.session.query(User.id) \
    	.join(UserTagAssoc) \
    	.filter(UserTagAssoc.tag_id==self.id))) \
    	.filter(UserTagAssoc.tag_id==Tag.id, Tag.id!=self.id) \
    	.group_by(Tag.id) \
    	.order_by(desc(func.count(UserTagAssoc.tag_id))) \
    	.all()

    def count(self):
    	return db.session.query(UserTagAssoc).filter(UserTagAssoc.tag_id==self.id).count()

    def prevalence(self):
    	return self.count() / db.session.query(User).count()


class GroupTagAssoc(db.Model):
    __tablename__ = 'group_tags'
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    group = db.relationship('Group', backref=backref('group_tags', cascade="all, save-update, merge, delete, delete-orphan"))
    tag = db.relationship('Tag', backref=backref('group_tags', cascade="all, save-update, merge, delete, delete-orphan"))
    timestamp = db.Column(db.DateTime())
    def __repr__(self):
        return '<GroupTagAssoc %r | %r>' % (self.group.name, self.tag.body)
  
  
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = association_proxy('group_tags', 'tag', creator=lambda x:GroupTagAssoc(tag=x, timestamp=datetime.utcnow()))

    def __repr__(self):
    	return '<Group %r>' % (self.name)
        
    def has_tag(self, tag):
        return db.session.query(Group).join(GroupTagAssoc).filter(GroupTagAssoc.group_id==self.id, GroupTagAssoc.tag_id==tag.id).count() > 0
        
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    pw_hash = db.Column(db.String(160))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    created_at = db.Column(db.DateTime)
    tags = association_proxy('user_tags', 'tag', creator=lambda x:UserTagAssoc(tag=x, timestamp=datetime.utcnow()))
    groups = db.relationship('Group', backref='user')

    def __init__(self, nickname, email, password, role=ROLE_USER):
    	self.nickname = nickname
    	self.email = email
    	self.pw_hash = User.hash_password(password)
    	self.role = role

    def __repr__(self):
    	return '<User %r>' % (self.nickname)

    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False

    def get_id(self):
    	return unicode(self.id)

    @staticmethod
    def nickname_taken(nickname):
    	return db.session.query(User).filter(User.nickname==nickname).count() > 0

    @staticmethod
    def email_taken(email):
    	return db.session.query(User).filter(User.email==email).count() > 0

    @staticmethod
    def user_for_nickname(nickname):
    	return db.session.query(User).filter(User.nickname==nickname).first()

    @staticmethod
    def user_for_email(email):
    	return db.session.query(User).filter(User.email==email).first()

    @staticmethod
    def hash_password(password):
    	return generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.pw_hash, password)

    def has_tag(self, tag):
    	return db.session.query(User).join(UserTagAssoc).filter(UserTagAssoc.user_id==self.id, UserTagAssoc.tag_id==tag.id).count() > 0

    def add_tag(self, tag, group=None):
        if group != None:
            group.tags.append(tag)
        if not self.has_tag(tag):
        	self.tags.append(tag)
        	return self

    def remove_tag(self, tag, group):
        if group.has_tag(tag):
            group.tags.remove(tag)
    	if self.has_tag(tag):
    		self.tags.remove(tag)
        db.session.commit()
    	return self

    def ordered_tags(self):
    	return db.session.query(Tag).join(UserTagAssoc).filter(UserTagAssoc.user_id==self.id).order_by(desc(UserTagAssoc.timestamp))

    def has_group(self, name):
        group = db.session.query(Group).join(User).filter(User.id==self.id, Group.name==name).first()
        if group:
            return True
        return False
        
    def get_group(self, name):
        if name == None:
            return None
        group = db.session.query(Group).join(User).filter(User.id==self.id, Group.name==name).first()
        return group
        
    def get_or_create_group(self, name):
        if name == None:
            return None
        group = db.session.query(Group).join(User).filter(User.id==self.id, Group.name==name).first()
        if group == None:
            group = Group(name=name)
            self.groups.append(group)
            db.session.add(group)
            db.session.commit()
        return group

    def tags_for_group(self, name):
        return db.session.query(Tag).join(GroupTagAssoc).join(Group).join(User).filter(User.id==self.id, Group.name==name).order_by(desc(GroupTagAssoc.timestamp))

    def remove_group(self, name):
        if self.has_group(name):
            group = self.get_group(name)
            self.groups.remove(group)
            db.session.commit()
        return self
