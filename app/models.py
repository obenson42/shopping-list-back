"""User ShoppingItem models for the Shopping List backend"""
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import html
import base64
import random
import string
from app import db, login

# function used by flask_login to get a user object
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# function used by flask_login to load a user via api_key param or Bearer in the Authorization header
@login.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if not api_key:
        api_key = request.form.get('api_key')
    if not api_key:
        data = request.get_json()
        if data is not None and "api_key" in data.keys():
            api_key = data["api_key"]
    if api_key:
        user = User.query.filter(User.api_key==api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth (I should probably be using JSON Web Tokens for this)
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Bearer ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
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
    password = Column(String(128), nullable=False) # password will be hashed when it is set
    spending_limit = Column(Integer, default=0, nullable=False) # in pence
    api_key = Column(String(64), default=''.join(random.choice(string.ascii_lowercase) for i in range(10)) + str(datetime.datetime.now())) # only created for new users, will be overwritten from db for existig users

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # convert an instance to a JSON representation (for passing to front end)
    # password is not included
    def jsonify(self):
        json = '{{"id":{}'.format(self.id)
        json += ',"username":"{}"'.format(html.escape(self.username))
        if self.email:
            json += ',"email":"{}"'.format(html.escape(self.email))
        json += ',"spending_limit":{}'.format(self.spending_limit)
        json += ',"api_key":"{}"'.format(self.api_key)
        json += '}'
        return json

    def __repr__(self):
        return '<User {}>'.format(self.username)

class ShoppingItem(db.Model):
    __tablename__ = 'shopping_item'
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    bought = Column(Integer, default=0, nullable=False) # 0 is not bought, 1 is bought (I was having problems with the Boolean column type)
    user_id = Column(Integer, index=True)
    position = Column(Integer, nullable=False)
    price = Column(Integer, nullable=True)

    # convert an instance to a JSON representation (for passing to front end)
    # user_id is not included as it is not needed at the front end and would make the system less secure
    def jsonify(self):
        json = '{{"id":{}'.format(self.id)
        json += ',"title":"{}"'.format(html.escape(self.title))
        json += ',"bought":1' if (self.bought == True or self.bought == 1) else ',"bought":0'
        json += ',"position":{}'.format(self.position)
        if self.price:
            json += ',"price":{}'.format(self.price)
        json += '}'
        return json

    def __repr__(self):
        return '<ShoppingItem: {} {}>'.format(self.id, self.title)
