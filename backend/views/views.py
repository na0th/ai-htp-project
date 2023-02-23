from flask import Blueprint, request, session, jsonify, redirect, url_for
from db_connect import db
import base64
from flask_cors import CORS
from models import User, EntireTree, TreeRoot, TreeBranch, TreeLeap, TreeStem, TreeSize
from model_predict import classification_multi, classification, detection #여기에 함수 다 넣음
import numpy as np
import tensorflow as tf
from flask import Flask

from PIL import Image
import io

#tf.keras lib
from tensorflow import keras
from keras.models import Model
from keras.applications.imagenet_utils import decode_predictions

#efficient lib
from efficientnet.keras import EfficientNetB3

#image, file lib
import cv2
import os

#df, np lib
import numpy as np
import pandas as pd

import json

from model_init import model_dict
from sqlalchemy import select

bp = Blueprint('views', __name__, url_prefix='/')
CORS(bp)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

@bp.route('/main/', methods=['POST', 'GET'])
def showMain():
    if request.method == 'POST': # POST
        '''
        request
            username
            ex) {"username": "yang"}
        '''
        params = request.get_json()

        # insert
        user = User(username=params['username'])
        db.session.add(user)
        db.session.commit()

        session['userid'] = user.userid

        print(model_dict)

        return jsonify({'message': 'The username is saved.', "userid": user.userid }), 200

@bp.route('/tree/', methods=['POST', 'GET'])
def showFirst():
    if request.method == 'POST':
        '''
        request
            ex) {"userid": "5", "image":""}
        '''
        session['step'] = 1

        params = request.get_json()
        userid = params['userid']
        session['userid'] = userid
        if userid == None:
            return redirect(url_for('views.showMain'))
        
        imgstr = params['image'][22:] 
        # print(params['image'])

        binaryimg = base64.b64decode(imgstr) # type: bytes

        # user = User.query.filter_by(userid).first()
        user = db.session.query(User).filter(User.userid == userid).first()
        user.image1 = binaryimg
        db.session.commit()

        # 모델 넣을 자리
        resultText = callTreeModel(binaryimg)
        return jsonify({'message': 'The image is saved.'}), 200

@bp.route('/home/', methods=['POST', 'GET'])
def showSecond():
    # if g.user == None:
    #     return redirect(url_for('views.showMain'))
    if request.method == 'POST':
        session['step'] = 2

        params = request.get_json()
        userid = params['userid']
        session['userid'] = userid
        if userid == None:
            return redirect(url_for('views.showMain'))
        
        imgstr = params['image'][22:] 
        # print(params['image'])

        binaryimg = base64.b64decode(imgstr) # type: bytes

        # user = User.query.filter_by(userid).first()
        user = db.session.query(User).filter(User.userid == userid).first()
        user.image2 = binaryimg
        db.session.commit()

        # 모델 넣을 자리
        callTreeModel(binaryimg)

        # user = User.query.filter_by(userid).first()
        user = db.session.query(User).filter(User.userid == userid).first()
        user.image2 = binaryimg
        db.session.commit()

        # 결과 넘겨주기 위한 코드
        str_base641 = base64.b64encode(user.image1)
        base64_str1 = str_base641.decode('utf-8')

        str_base642 = base64.b64encode(user.image2)
        base64_str2 = str_base642.decode('utf-8')

        return jsonify({
            "username": user.username,
            "image1": 'data:image/png;base64,' + base64_str1,
            "image2": 'data:image/png;base64,' + base64_str2,
            "tree": {
                "entiretree": json.loads(user.entiretree),
                "treeroot": json.loads(user.treeroot),
                "treebranch": json.loads(user.treebranch),
                "treeleap": json.loads(user.treeleap),
                "treestem": json.loads(user.treestem),
                "treesize": json.loads(user.treesize)
            },
            "home": {
                "temporarykey": "temporaryvalue"
            }
        }), 200

@bp.route('/test/', methods=['POST', 'GET'])
def test():
    resultJson = {}
    resultData = db.session.query(EntireTree).filter(EntireTree.id == 0).first()
    if resultData is not None:
        tmp = resultData.result
        print(type(tmp))
        tmpsplit = resultData.result.split(':')
        print(tmpsplit)
        subtitle = tmpsplit[0]
        print(subtitle)
        print(type(subtitle))
        result = tmpsplit[1]
        print(result)
        print(type(result))
        resultJson[subtitle]=result
    print(json.dumps(resultJson))
    print(json.loads(json.dumps(resultJson)))

    return json.dumps(resultJson)

def callTreeModel(binaryimg):
    user = db.session.query(User).filter(User.userid == session['userid']).first()

    #######수정 및 추가 내용########
    #######원래 가지, 줄기, 뿌리, 나무 타입 모델이었던 것은 멀티라벨 모델로 진행하여 모델 수를 줄이려고 했었는데
    #######그랬더니 정확도가 낮게 나와서 가지 모델 2개, 줄기 모델 2개, 잎열매 모델 4개, 뿌리 모델 1개, 나무 타입 모델 1개 예정
    #######아래의 코드처럼 classification(모델이름, 이미지, 사이즈(input size에 맞게 설정해둘 예정)) 함수만 추가하면 됨
    # result_treeType = classification('tree_type', './image/1004.png', 300) #나무 타입
    # result_flower = classification('flower', './image/1001.png', 300) #꽃 유무. 없다 0, 있다 1 
    # result_fruit = classification('fruit', './image/1001.png', 300) #열매 유무. 없다 0, 있다 1
    #################################

    # 0. tree_size_location
    treesizeResult = detection(binaryimg) # 경로에서 불러온 이미지를 request 메시지에서 받은 이미지로 변경할 것    
    user.treesize = save_result(TreeSize, treesizeResult)

    # 1. tree_type 나무 전체 => 0 1 2 3 4 중에 하나 
    if user.crop1_1004 is not None:
        entiretreeResult=[]
        entiretreeResult.append(classification('tree_type', user.crop1_1004, 300))
        user.entiretree = save_result(EntireTree, entiretreeResult)

    # if user.crop1_1001 is not None:
    # # 2. 3. 잎, 열매, 꽃, 가지
    #     branch_leaf_li = ['열매있음','윗쪽으로 뻗는','잎이 안 큰','잎무성한','꽃있음', '그물', '잎이 큰']
    #     result_leaf_branch = classification_multi('leaf_branch', user.crop1_1001, branch_leaf_li, 200, 7)
    #     leapResult=[]
    #     if '열매있음' in result_leaf_branch:
    #         leapResult.append(3)
    #     if '잎무성한' in result_leaf_branch:
    #         leapResult.append(1)
    #     if '잎이 큰' in result_leaf_branch:
    #         leapResult.append(0)
    #     if '꽃있음' in result_leaf_branch:
    #         leapResult.append(2)
    #     user.treeleap = save_result(TreeLeap, leapResult)
    
    #     branchResult=[]
    #     if '윗쪽으로 뻗는' in result_leaf_branch:
    #         branchResult.append(1)
    #     if '그물' in result_leaf_branch:
    #         branchResult.append(0)
    #     user.treebranch = save_result(TreeBranch, branchResult)
    
    if user.crop1_1002 is not None:
        # 4. stem 줄기 => [0, 0, 0]
        stemResult=[]
        stemResult.append(classification('stem', user.crop1_1002, 300))
        user.treestem = save_result(TreeStem, stemResult)

    if user.crop1_1003 is not None:
        # 5. root 뿌리 => 1 2 3 4 5 중에 하나
        rootResult=[]
        rootResult.append(classification('root', user.crop1_1003, 300))
        user.treeroot = save_result(TreeRoot, rootResult)

    db.session.commit()
    # return result
    # return resultStr

def save_result(table, result): # db테이블과 찾고자하는 id 값 받고 resultStr에 저장
    '''
   	id int,
	subtitle text,
	result text
    '''
    resultJson = {}
    resultStr = ""
    for id in result:
        print("*************")
        print(id)
        # resultData = table.query.filter_by(id).first()
        resultData = db.session.query(table).filter(table.id == id).first()
        if resultData is not None:
            tmp = resultData.result
            print(type(tmp))
            print(tmp)
            tmpsplit = resultData.result.split(":")
            print(tmpsplit)
            subtitle = tmpsplit[0]
            print(subtitle)
            print(type(subtitle))
            result = tmpsplit[1]
            print(result)
            print(type(result))
            resultJson[subtitle]=result
            # resultJson['{}'.format(resultData.subtitle)] = resultData.result
        # resultStr += (resultData.result + '\n')
    return json.dumps(resultJson)