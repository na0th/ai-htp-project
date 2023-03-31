# standard library imports
# Third party imports
from flask import (Blueprint, jsonify, request, session)
from flask_cors import CORS
# local application imports
from db_connect import db
from backend.app.main.model.repository.user.user_repository import *

bp = Blueprint('main', __name__, url_prefix='/')
CORS(bp, resources={r"*": {"origins": "*"}})

@bp.route('/main/', methods=['POST', 'GET'])
def show_main_page():
    if request.method == 'POST':
        params = request.get_json()
        
        session['user_id'] = save_user(params['username'])

        return jsonify({'message': 'The username is saved.', 'user_id': session['user_id'] }), 200

