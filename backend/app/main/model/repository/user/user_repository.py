from main.config.db_connect import db
from main.model.domain.user.user_model import *

def save_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user.userid

def save_user_tree(userid, result):
    user_tree = UserTree(userid=userid)
    user_tree.treetype = result.type
    user_tree.treeroot = result.root
    user_tree.treebranch = result.branch
    user_tree.treeleap = result.leap
    user_tree.treestem = result.stem
    user_tree.treesize = result.size
    db.session.add(user_tree)
    db.session.commit()

def save_user_house(userid, result):
    user_house = UserHouse(userid=userid)
    user_house.housetype = result.type
    user_house.houseroof = result.roof
    user_house.housedoor = result.door
    user_house.housewindow = result.window
    db.session.add(user_house)
    db.session.commit()

def find_user(userid):
    return db.session.query(User).filter(User.userid == userid).first()

def find_user_tree_result(userid):
    return db.session.query(UserTree).filter(UserTree.userid == userid).first()

def find_user_house_result(userid):
    return db.session.query(UserHouse).filter(UserHouse.userid == userid).first()

def update_user_draw(userid, img_binary, step):
    user = find_user(userid)
    if step == 1:
        user.treeimg = img_binary
    elif step == 2:
        user.houseimg = img_binary
    db.session.commit()

def update_user_tree_crop(class_id, userid, npbinary):
    user = find_user(userid)
    if class_id == 1.0:
        user.tree1001 = npbinary
    elif class_id == 2.0:
        user.tree1002 = npbinary
    elif class_id == 3.0:
        user.tree1003 = npbinary
    else: # class_id == 4.0
        user.tree1004 = npbinary
    db.session.commit()