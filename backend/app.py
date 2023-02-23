from flask import Flask, g
from db_connect import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:8080"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1234@127.0.0.1:3306/ai-htp-test"
app.config['SQLARCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ekdwls'

db.init_app(app)

import tensorflow as tf

# 블루프린트
from views import views
app.register_blueprint(views.bp)

if __name__ == '__main__':
    app.run(port=3000, debug=True)

# with app.app_context():
#     g.model_dict = {
#         "detection": tf.saved_model.load('.\model\detection\saved_model'),
#         "leaf_branch": tf.keras.models.load_model('./model/classification/leaf_branch.h5'),
#         "tree_type": tf.keras.models.load_model('./model/classification/tree_type.h5')
#     }
#     print(g.model_dict)