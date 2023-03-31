# standard library imports
# Third party imports
from flask import Flask, g
from flask_cors import CORS
# local application imports
from db_connect import db
from backend.app.main.controller.api.draw_controller import draw
from backend.app.main.controller.api.main_controller import main

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/ai-htp-test"
app.config['SQLARCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)

app.register_blueprint(main.bp)
app.register_blueprint(draw.bp)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
