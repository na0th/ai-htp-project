from main.config.db_connect import db

# 집 db class
class HouseType(db.Model):
	__tablename__ = 'house_type'
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