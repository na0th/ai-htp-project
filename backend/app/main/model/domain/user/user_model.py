from main.config.db_connect import db

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    treeimg = db.Column(db.BLOB)
    houseimg = db.Column(db.BLOB)
    tree1001 = db.Column(db.BLOB)
    tree1002 = db.Column(db.BLOB)
    tree1003 = db.Column(db.BLOB)
    tree1004 = db.Column(db.BLOB)    

class UserTree(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    treetype = db.Column(db.TEXT)
    treeroot = db.Column(db.TEXT)
    treebranch = db.Column(db.TEXT)
    treeleap = db.Column(db.TEXT)
    treestem = db.Column(db.TEXT)
    treesize = db.Column(db.TEXT)

class UserHouse(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    housetype = db.Column(db.TEXT)
    houseroof = db.Column(db.TEXT)
    housedoor = db.Column(db.TEXT)
    housewindow = db.Column(db.TEXT)
	