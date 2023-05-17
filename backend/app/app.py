# standard library imports
# Third party imports
from flask import Flask
from flask_cors import CORS
# local application imports
from main.config.db_connect import db
from main.controller.api.draw_controller import bp as drawbp
from main.controller.api.main_controller import bp as mainbp

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/ai_htp_test"
app.config['SQLARCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)

app.register_blueprint(mainbp)
app.register_blueprint(drawbp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
