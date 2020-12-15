"""User ShoppingItem models for the Shopping List backend"""
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import html
import base64
from app import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@login.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth (I should probably be using JSON Web Tokens for this)
    api_key = request.headers.get('ShoppingItemization')
    if api_key:
        api_key = api_key.replace('Bearer ', '', 1)
        #try:
        #    api_key = base64.b64decode(api_key)
        #except TypeError:
        #    pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

class User(UserMixin, db.Model):
    __tablename__ = 'user_stuff'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(128), index=True, unique=True)
    password = Column(String(128), nullable=False)
    spending_limit = Column(Numeric(10, 2), nullable=False)
    api_key = "not a sensible API key"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def jsonify(self):
        json = '{"id":' + str(self.id)
        json += ',"username":"' + html.escape(self.username) + '"'
        if self.email:
            json += ',"email":"' + html.escape(self.email) + '"'
        json += ',"spending_limit:"' + str(self.spending_limit)
        json += ',"api_key":"' + self.api_key + '"'
        json += '}'
        return json

    def __repr__(self):
        return '<User {}>'.format(self.username)

class ShoppingItem(db.Model):
    __tablename__ = 'shopping_item'
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    bought = Column(Boolean, nullable=False)
    user_id = Column(Integer, index=True)
    position = Column(Integer, nullable=False)

    def jsonify(self):
        json = '{"id":' + str(self.id)
        json += ',"title":"' + html.escape(self.title) + '"'
        json += ',"bought":"' + self.bought + '"'
        json += ',"user_id:"' + str(self.user_id)
        json += ',"position:"' + str(self.position)
        json += '}'
        return json

    def __repr__(self):
        return '<ShoppingItem: {}>'.format(self.surname)
