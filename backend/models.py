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
    crop2_1001 = db.Column(db.BLOB)
    crop2_1002 = db.Column(db.BLOB)
    crop2_1003 = db.Column(db.BLOB)
    crop2_1004 = db.Column(db.BLOB)
    result1 = db.Column(db.TEXT)
    result2 = db.Column(db.TEXT)

# 나무 db class
class EntireTree(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
        
class TreeRoot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
class TreeBranch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
class TreeLeap(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
class TreeStem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
class TreeSize(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
# 집 db class
class HouseRoof(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
class HouseDoor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)
	
class HouseWindow(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	subtitle = db.Column(db.TEXT)
	result = db.Column(db.TEXT)