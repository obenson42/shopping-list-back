from flask import Blueprint

bp = Blueprint('mock_tesco', __name__, url_prefix='/mock_tesco')

from app.mock_tesco import routes
