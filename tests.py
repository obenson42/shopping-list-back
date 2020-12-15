from datetime import datetime, timedelta
import unittest
from flask import make_response
from flask_api import status
from app import create_app, db, cache
from app.models import User, ShoppingItem
from app.shopping_list import ShoppingListDB
from config import Config
import json

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    # create the app with a test config and push its context (usually done by flask)
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # clean up - remove all db stuff and pop the app context
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    ### User tests
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))


class ShoppingItemModelCase(unittest.TestCase):
    # create the app with a test config and push its context (usually done by flask)
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # create shoppingitem db object
        self.shoppingListDB = ShoppingListDB(db, cache)

    # clean up - remove all db stuff and pop the app context
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_shoppingitem_crud(self):
        # create an shoppingitem and store it
        a1 = ShoppingItem(title="Bananas")
        self.shoppingListDB.create(None, a1) # SQLAlchemy will put the id of the created record in the ShoppingItem instance
        self.assertTrue(a1.id != None)

        # read the shoppingitem
        resp = self.shoppingListDB.get(a1.id)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        # update the shoppingitem
        a1.first_name = "Lettuce"
        resp = self.shoppingListDB.update(None, a1)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)

        # delete the shoppingitem
        resp = self.shoppingListDB.delete(a1.id)
        self.assertTrue(resp.status_code == status.HTTP_200_OK)
        # try to read the shoppingitem
        resp = self.shoppingListDB.get(a1.id)
        self.assertTrue(resp.status_code == status.HTTP_404_NOT_FOUND)

if __name__ == '__main__':
    unittest.main(verbosity=2)
