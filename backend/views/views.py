from flask import Blueprint, request, session, jsonify, redirect, url_for
from db_connect import db
import base64
from flask_cors import CORS
from models import User, EntireTree, TreeRoot, TreeBranch, TreeLeap, TreeStem, TreeSize
from model_predict import classification_multi, classification, detection #여기에 함수 다 넣음
from model_init import model_
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
                "entiretree": user.entiretree,
                "treeroot": user.treeroot,
                "treebranch": user.treebranch,
                "treeleap": user.treeleap,
                "treestem": user.treestem,
                "treesize": user.treesize
            },
            "home": {
                "temporarykey": "temporaryvalue"
            }
        }), 200

def predict():

    detection('./image/test_3.PNG') #경로에서 불러온 이미지를 request 메시지에서 받은 이미지로 변경할 것

    #######수정 및 추가 내용########

    branch_leaf_li = ['열매있음','윗쪽으로 뻗는','잎이 안 큰','잎무성한','꽃있음', '그물', '잎이 큰']
    result_leaf_branch = classification_multi('leaf_barnch', './image/1001.png', branch_leaf_li, 200, 7)
    #################################

    return result_leaf_branch   

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
    user.treesize = save_result(EntireTree, treesizeResult)

    # 1. tree_type 나무 전체 => 0 1 2 3 4 중에 하나 
    entiretreeResult = classification('tree_type', user.crop1_1004, 300)
    user.entiretree = save_result(TreeSize, entiretreeResult)
    # 2. branch 가지 => [0, 0, 0]
    # 3. leap 잎, 열매 => [0, 0, 0, 0]
    # leapResult = []
    # result_flower = classification('flower', user.crop1_1001, 300) #꽃 유무. 없다 0, 있다 1 
    # result_fruit = classification('fruit', user.crop1_1001, 300) #열매 유무. 없다 0, 있다 1
    # leapResult.append(result_flower)
    # leapResult.append(result_fruit)
    # 인덱스로 변환해서 들어가야 됨
    # user.treeleap = save_result(TreeLeap, leapResult)

    # 2. 3. 잎, 열매, 꽃, 가지
    branch_leaf_li = ['열매있음','윗쪽으로 뻗는','잎이 안 큰','잎무성한','꽃있음', '그물', '잎이 큰']
    result_leaf_branch = classification_multi('leaf_branch', user.crop1_1001, branch_leaf_li, 200, 7)
    leapResult=[]
    if '열매있음' in result_leaf_branch:
        leapResult.append(3)
    if '잎무성한' in result_leaf_branch:
        leapResult.append(1)
    if '잎이 큰' in result_leaf_branch:
        leapResult.append(0)
    if '꽃있음' in result_leaf_branch:
        leapResult.append(2)
    user.treeleap = save_result(TreeLeap, leapResult)
    
    branchResult=[]
    if '윗쪽으로 뻗는' in result_leaf_branch:
        branchResult.append(1)
    if '그물' in result_leaf_branch:
        branchResult.append(0)
    user.treebranch = save_result(TreeBranch, branchResult)
    
    # 4. stem 줄기 => [0, 0, 0]
    stemResult=[]
    stemResult.append(classification('stem', user.crop1_1002, 300))
    user.treestem = save_result(TreeStem, stemResult)

    # 5. root 뿌리 => 1 2 3 4 5 중에 하나
    rootResult=[]
    rootResult.append(classification('root', user.crop1_1003, 300))
    user.treeroot = save_result(TreeRoot, rootResult)

    db.session.commit()
    # return result
    # return resultStr

def save_result(table, result): # db테이블과 찾고자하는 id 값 받고 resultStr에 저장
    # print(result)
    resultStr = ''
    for index in result:
        resultData = db.session.query(table).filter(table.id == index).first()
        if resultData is not None:
            resultStr += (resultData.result + '\n')
    return resultStr
    
'''
# detection function
def detection(binaryimg):
    resultlist = []
    
    encoded_img = np.fromstring(binaryimg, dtype = np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 이미지를 읽고 rgb로 변환한다. (opencv는 bgr로 읽음)
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.uint8)[tf.newaxis, ...] # 텐서 형식으로 변환
    
    # print(img)
    # print(np.array(img))

    height = img_array.shape[0]
    width = img_array.shape[1]

    draw_img = img_array.copy()

    #모델 로드
    model = tf.saved_model.load('.\model\detection\saved_model')

    #사용자 이미지 추론 (detection)
    result = model(img_tensor)
    result = {key:value.numpy() for key,value in result.items()}
    
    #임계값 지정. 50% 이상일 때만 바운딩박스 그림
    SCORE_THRESHOLD = 0.5
    OBJECT_DEFAULT_COUNT = 4 #클래스 개수

    #클래스 매칭
    labels_to_names = {1.0:'1001', 2.0:'1002', 3.0:'1003', 4.0:'1004'}


    for i in range(min(result['detection_scores'][0].shape[0], OBJECT_DEFAULT_COUNT)):
        score = result['detection_scores'][0,i]
        print(i)
        if score < SCORE_THRESHOLD: #임계값보다 작을 경우 break
            break
        box = result['detection_boxes'][0,i]
        left = box[1] * width
        top = box[0] * height
        right = box[3] * width
        bottom = box[2] * height
        class_id = result['detection_classes'][0, i]

        crop_img = draw_img[int(top):int(bottom),int(left):int(right)] #detection 하여 그린 박스만큼 이미지 크롭
        
        # numpy -> str
        # npstr = np.array2string(crop_img)
        # str -> numpy
        # nparr = np.array(str)

        ########### 추가
        if labels_to_names[class_id] == '1004': # 1004면
            tree_height = bottom-top
            tree_width = right-left
            resultlist.extend(tree_size_loc(height, width, top, bottom, left, right))
            # print('location',location)
        elif labels_to_names[class_id] == '1002':
            stem_height = bottom-top
            stem_width = right-left
        ###########

        npImage = Image.fromarray(crop_img)
        img_byte_arr = io.BytesIO()
        npImage.save(img_byte_arr, format='jpeg')
        img_byte_arr = img_byte_arr.getvalue()

        # crop한 이미지 db에 저장한다.
        cropimgToDB(class_id, img_byte_arr)
        # cv2.imwrite('./image/'+labels_to_names[class_id]+'.png',cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)) #크롭하여 로컬에 저장 (저장 안 하는 방식으로 수정?)

        print('class_id', class_id)

        caption = "{}: {:.4f}".format(labels_to_names[class_id], score)
        print(caption)  #score 콘솔에서 확인
    
    ################
    # 줄기 사이즈
    # stem_size = 0 #보통이다
    if stem_height > tree_height * (1/2):
        # stem_size = 2 #길다
        resultlist.append(4)
    elif stem_height < tree_height * (1/6):
        stem_size = 1  #짧다
        resultlist.append(5)

    # 줄기 굵기
    stem_thickness = 0 #보통이다
    if stem_width  < tree_width/10:
        stem_thickness = 1 # 얇다
        resultlist.append(7)
    elif stem_width > tree_width * 0.23:
        stem_thickness = 2 # 굵다
        resultlist.append(6)
    ##########    
    return resultlist

def cropimgToDB(class_id, npbinary):
    userid = session['userid']
    user = db.session.query(User).filter(User.userid == userid).first()
    # 이거 있는지 업는지 확인해야돼
    if session['step'] == 1:
        if class_id == 1.0:
            user.crop1_1001 = npbinary
        elif class_id == 2.0:
            user.crop1_1002 = npbinary
        elif class_id == 3.0:
            user.crop1_1003 = npbinary
        else: # class_id == 4.0
            user.crop1_1004 = npbinary
    else: # g.step == 2:
        if class_id == 1.0:
            user.crop2_1001 = npbinary
        elif class_id == 2.0:
            user.crop2_1002 = npbinary
        elif class_id == 3.0:
            user.crop2_1003 = npbinary
        else: # class_id == 4.0
            user.crop2_1004 = npbinary
    db.session.commit()

#classification funcation
def classification(model_file_name, binaryimg):
    # model_file_name: str
    # img: np array
    # 예시: 나무 타입 분류
    treeType_model = tf.keras.models.load_model('./model/classification/'+model_file_name+'.h5') #모델 로드

    encoded_img = np.fromstring(binaryimg, dtype = np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 아까 잘라서 저장한 나무 전체 이미지 불러온다
    image = cv2.resize(img_array, dsize=(300, 300)) # 리사이징
    test_image = np.array(image) # np array type으로 변경
    test_image = np.expand_dims(test_image, axis=0) # 차원 추가
    test_image.shape # shape확인

    # print(type(img_path)) # <class 'str'>
    # print(type(cv2.imread(img_path))) # <class 'numpy.ndarray'>
    # print(type(img_array)) # <class 'numpy.ndarray'>
    # print(type(image)) # <class 'numpy.ndarray'>

    prediction = treeType_model.predict(test_image) #추론
    tree_type = np.argmax(prediction) #결과 확인. 0: 상록수
    return str(tree_type)

def tree_size_loc(height, width, top, bottom, left, right): ## 새로 생성
    # tree_size, tree_location

    treesizeResult = []

    img_size = height*width
    tree_size = (bottom-top)*(right-left) # 트리 크기
    img_center = width / 2 # 그림 중앙 좌표
    tree_center = left + ((right-left)/2) # 트리 중앙 좌표

    # tree size: 0 1
    # tree_size_flag = 0 # 보통, 크다

    if tree_size < img_size / 4:
        treesizeResult.append(0)
    
    # tree location: 0 1 2
    if tree_center < img_center / 2:
        # tree_location = 0 # left
        treesizeResult.append(1)
    elif tree_center > img_center * 1.5:
        tree_location = 2 # right
        treesizeResult.append(3)
    else:
        tree_location = 1 # center
        treesizeResult.append(2)
    return treesizeResult
'''