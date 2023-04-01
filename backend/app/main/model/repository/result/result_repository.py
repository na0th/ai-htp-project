from main.model.domain.result.house_model import *
from main.model.domain.result.tree_model import *
from main.config.db_connect import db

def find_result(table, id):
    return db.session.query(table).filter(table.id == id).first()
