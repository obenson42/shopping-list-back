from flask import (
    Blueprint, request, make_response
)
from flask_api import status
from flask_cors import CORS, cross_origin
from werkzeug.urls import url_parse
import json
import random

from app.mock_tesco import bp

# replacement for Tesco API until they allow access again
@bp.route('/products/', methods=['GET'])
@cross_origin()
def get_products():
    query = request.args.get('query')
    # ensure it's lowercase
    if query != '':
        query = query.lower()
    # remove any trailing 'es' or 's'
    if query[-2:] == 'es':
        query = query[:-2]
    elif query[-1] == 's':
        query = query[:-1]
    products_found = ''
    with open('app/mock_tesco/groceries.json') as json_file:
        products = json.load(json_file)
        for p in products:
            if p['name'] == query:
                products_found = '{"uk": {"ghs": {"products": {"results": ['
                for r in p['results']:
                    products_found += json.dumps(r) + ','
                products_found = products_found[:-1]  # remove extra comma
                products_found += ']} } } }'
    # if no product is found, create dummy with given query, random id and price
    if products_found == '':
        products_found = '{"uk": {"ghs": {"products": {"results": [{"id": ' + str(random.randrange(1, 1000)) + ', "title": "' + query + '", "price": ' + str(random.randrange(1, 1000) / 100.0) + '}]}}}}'
    return make_response(
        products_found,
        status.HTTP_200_OK,
        {"Content-Type": "application/json"})
