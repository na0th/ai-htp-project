from model.domain.result.house_model import *
from model.domain.result.tree_model import *
from db_connect import db

def find_result(table, id):
    return db.session.query(table).filter(table.id == id).first()
