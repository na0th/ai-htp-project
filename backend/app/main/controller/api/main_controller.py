# standard library imports
# Third party imports
from flask import (Blueprint, jsonify, request, session)
from flask_cors import CORS
# local application imports
from main.config.db_connect import db
from main.model.repository.user.user_repository import *

bp = Blueprint('main', __name__, url_prefix='/')
CORS(bp, resources={r"*": {"origins": "*"}})

@bp.route('/main/', methods=['POST', 'GET'])
def show_main_page():
    if request.method == 'POST':
        params = request.get_json()
        
        session['id'] = save_user(params['name'])

        return jsonify({'message': 'The name is saved.', 'id': session['id'] }), 200

