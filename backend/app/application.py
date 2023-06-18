# standard library imports
# Third party imports
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse
from flask_swagger_ui import get_swaggerui_blueprint
# local application imports
from main.config.db_connect import db
from main.controller.api.draw_controller import bp as drawbp
from main.controller.api.main_controller import bp as mainbp

application = Flask(__name__)
CORS(application, resources={r"*": {"origins": "*"}})

application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/ai_htp_test"
application.config['SQLARCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'ekdwls'

db.init_app(application)

api = Api(application, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

application.register_blueprint(mainbp)
application.register_blueprint(drawbp)

if __name__ == '__main__':
    application.run(port=5000, debug=True)
