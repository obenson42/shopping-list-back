""" API for CRUD methods on ShoppingItems """
from flask import make_response
from flask_api import status
import datetime

from app.models import ShoppingItem
from app.utilities import jsonifyList

class ShoppingItemDB:
    """ class to handle requests from api for shopping items """

    def __init__(self, db):
        self.db = db
        self.headers = {"Content-Type": "application/json"}

    # get all ShoppingItems for the given user_id, returns JSON formatted list
    def get_all(self, user_id):
        shoppingitems = ShoppingItem.query.order_by(ShoppingItem.position).all()
        json = jsonifyList(shoppingitems, "shopping_items")
        return make_response(
            json,
            status.HTTP_200_OK,
            self.headers)

    # create new shoppingitem from form data or ShoppingItem instance => JSON dictionary with success or fail status
    def create(self, shoppingitem):
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
    def update(self, shoppingitem):
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
    def delete(self, id, user_id):
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

    # update the given item's position and all other items between new and old positions => JSON with success or fail status
    def reorder_items(self, id, new_position):
        # check shoppingitem has id (so exists in db)
        if not id:
            # return fail
            json = '{"id":' + str(id) + ', "operation":"update author", "status":"fail"}'
            return make_response(
                json,
                status.HTTP_404_NOT_FOUND,
                self.headers)
        # get existing item
        # hold onto old position
        # get all items from new position to old position (or vice versa)
        # update each item with new position
        # return success
        json = '{"operation":"reorder", "status":"success"}'
        return make_response(
            json,
            status.HTTP_200_OK,
            self.headers)
