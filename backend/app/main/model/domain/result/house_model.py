from db_connect import db

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