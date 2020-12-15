""" API for CRUD methods on ShoppingItems """
from flask import make_response
from flask_api import status
import datetime

from app.models import ShoppingItem
from app.utilities import jsonifyList

class ShoppingItemDB:
    """ class to handle requests from api for shopping items """

    def __init__(self, db, cache):
        self.db = db
        self.cache = cache
        self.headers = {"Content-Type": "application/json"}

    # get all ShoppingItems for the given user_id, returns JSON formatted list
    def get_all(self, user_id):
        shoppingitems = ShoppingItem.query.all()
        json = jsonifyList(shoppingitems, "shopping_items")
        return make_response(
            json,
            status.HTTP_200_OK,
            self.headers)

    # create new shoppingitem from form data or ShoppingItem instance => JSON dictionary with success or fail status
    def create(self, form, shoppingitem=None):
        # add the shoppingitem
        self.db.session.add(shoppingitem)
        self.db.session.commit()
        # return success
        json = '{"id":' + str(shoppingitem.id) + ', "operation":"create shoppingitem", "status":"success"}'
        return make_response(
            json,
            status.HTTP_201_CREATED,
            self.headers)

    # update existing shoppingitem from ShoppingItem instance => JSON with success or fail status
    def update(self, form, shoppingitem=None):
        # check shoppingitem has id (so exists in db)
        if not shoppingitem.id:
            # return fail
            json = '{"id":' + str(shoppingitem.id) + ', "operation":"update author", "status":"fail"}'
            return make_response(
                json,
                status.HTTP_404_NOT_FOUND,
                self.headers)
        # update ShoppingItem in db
        ShoppingItem.query.filter(ShoppingItem.id==shoppingitem.id).\
            update({ "title":shoppingitem.title, "bought":shoppingitem.bought, "position":shoppingitem.position })
        self.db.session.commit()
        # return success
        json = '{"id":' + str(shoppingitem.id) + ', "operation":"update shoppingitem", "status":"success"}'
        return make_response(
            json,
            status.HTTP_200_OK,
            self.headers)
 
    # delete existing shoppingitem => JSON with success or fail status
    def delete(self, id):
        if not id:
            # return fail
            json = '{"id":' + str(id) + ', "operation":"delete", "status":"fail"}'
            return make_response(
                json,
                status.HTTP_404_NOT_FOUND,
                self.headers)
        
        ShoppingItem.query.filter(ShoppingItem.id == id).delete()
        self.db.session.commit()
        # return success
        json = '{"id":' + str(id) + ', "operation":"delete", "status":"success"}'
        return make_response(
            json,
            status.HTTP_200_OK,
            self.headers)
