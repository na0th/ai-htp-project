from db_connect import db
from datetime import datetime

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    image1 = db.Column(db.BLOB)
    image2 = db.Column(db.BLOB)
    crop1_1001 = db.Column(db.BLOB)
    crop1_1002 = db.Column(db.BLOB)
    crop1_1003 = db.Column(db.BLOB)
    crop1_1004 = db.Column(db.BLOB)
    entiretree = db.Column(db.TEXT)
    treeroot = db.Column(db.TEXT)
    treebranch = db.Column(db.TEXT)
    treeleap = db.Column(db.TEXT)
    treestem = db.Column(db.TEXT)
    treesize = db.Column(db.TEXT)
    houseroof = db.Column(db.TEXT)
    housedoor = db.Column(db.TEXT)
    housewindow = db.Column(db.TEXT)
    entirehouse = db.Column(db.TEXT)
	

# 나무 db class
class EntireTree(db.Model):
	__tablename__ = 'entire_tree'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
        
class TreeRoot(db.Model):
	__tablename__ = 'tree_root'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
class TreeBranch(db.Model):
	__tablename__ = 'tree_branch'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
class TreeLeap(db.Model):
	__tablename__ = 'tree_leap'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
class TreeStem(db.Model):
	__tablename__ = 'tree_stem'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
class TreeSize(db.Model):
	__tablename__ = 'tree_size'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
# 집 db class
class EntireHouse(db.Model):
	__tablename__ = 'entire_house'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)

class HouseRoof(db.Model):
	__tablename__ = 'house_roof'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
class HouseDoor(db.Model):
	__tablename__ = 'house_door'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)
	
class HouseWindow(db.Model):
	__tablename__ = 'house_window'
	id = db.Column(db.Integer, primary_key=True)
	result = db.Column(db.TEXT)