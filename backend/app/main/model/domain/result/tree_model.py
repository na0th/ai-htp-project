from db_connect import db

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