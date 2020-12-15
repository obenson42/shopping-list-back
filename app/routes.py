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
    return shoppingItemDB.get_all(current_user.user_id)

# create new shopping item
@bp.route('/item/', methods=['PUSH'])
@login_required
def item_create():
    form = ShoppingItemForm(request.form)
    return shoppingItemDB.create(form, current_user.user_id)

# update existing shopping item
@bp.route('/item/', methods=['PUT'])
@login_required
def item_update():
    form = ShoppingItemForm(request.form)
    return shoppingItemDB.update(form, current_user.user_id)
 
# delete existing shopping item
@bp.route('/item/<int:id>', methods=['DELETE'])
@login_required
def item_delete(id):
    return shoppingItemDB.delete(id, current_user.user_id)

@bp.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(basedir, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
