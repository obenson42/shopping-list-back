import os
basedir = os.path.abspath(os.path.dirname(__file__))

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, make_response, request, session, url_for, send_from_directory
)
from flask_login import login_required, current_user
from flask_cors import CORS, cross_origin

import datetime

from app import db
from app.models import User, ShoppingItem
from app.forms import ShoppingItemForm
from app.ShoppingItemDB import ShoppingItemDB

bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')
shoppingItemDB = ShoppingItemDB(db)

@bp.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'https://obenson-shopping-list.herokuapp.com'
    #header['Access-Control-Allow-Origin'] = 'http://localhost:9000'
    return response

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    html = render_template("home.html")
    return html

## API for Single Page Application
## all of these requests return JSON

## shopping item routes
# get all shopping items
@bp.route('/items/', methods=['GET'])
@login_required
@cross_origin()
def get_all_items():
    return shoppingItemDB.get_all()

# create new shopping item
@bp.route('/item/', methods=['POST'])
@login_required
@cross_origin()
def item_create():
    data = request.get_json()
    item = data["item"]
    shoppingItem = ShoppingItem(title=item["title"], bought=int(item["bought"]), position=item["position"], user_id=current_user.get_id())
    return shoppingItemDB.create(shoppingItem)

# update existing shopping item
@bp.route('/item_update/', methods=['POST'])
@login_required
@cross_origin()
def item_update():
    data = request.get_json()
    item = data["item"]
    shoppingItem = ShoppingItem(id=item["id"], title=item["title"], bought=item["bought"], position=item["position"], user_id=current_user.get_id())
    return shoppingItemDB.update(shoppingItem)
 
# update existing shopping item's position (this will affect multiple items)
# takes one item which is the one the user repositioned, other item's position can be worked out from that
@bp.route('/reorder/', methods=['POST'])
@login_required
@cross_origin()
def reorder_items():
    data = request.get_json()
    item = data["item"]
    return shoppingItemDB.reorder_items(item["id"], item["position"])
 
# delete existing shopping item
@bp.route('/item/', methods=['DELETE'])
@login_required
@cross_origin()
def item_delete():
    data = request.get_json()
    item = data["item"]
    return shoppingItemDB.delete(item["id"])

@bp.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(basedir, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
