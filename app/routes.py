import os
basedir = os.path.abspath(os.path.dirname(__file__))

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, make_response, request, session, url_for, send_from_directory
)
from flask_login import login_required, current_user
from flask_cors import CORS, cross_origin

import datetime

from app import db, cache
from app.models import User, ShoppingItem
from app.ShoppingList import ShoppingItemDB

bp = Blueprint('main', __name__)
shoppingItemDB = ShoppingItemDB(db, cache)

@bp.route('/')
@bp.route('/index')
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

# create new book
@bp.route('/item/', methods=['PUSH'])
@login_required
def item_create():
    form = BookForm(request.form)
    return shoppingItemDB.create(form)

# update existing book
@bp.route('/item/', methods=['PUT'])
@login_required
def item_update():
    form = BookForm(request.form)
    return shoppingItemDB.update(form)
 
# delete existing book
@bp.route('/item/<int:id>', methods=['DELETE'])
@login_required
def item_delete(id):
    return shoppingItemDB.delete(id)

@bp.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(basedir, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
