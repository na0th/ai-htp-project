from flask import session, g

import tensorflow as tf
import numpy as np

#tf.keras lib
from tensorflow import keras
from keras.models import Model

#image, file lib
import cv2
import os

#numpy lib
import numpy as np

#efficient lib
from efficientnet.keras import EfficientNetB3

from tree_size import tree_size_loc

from PIL import Image
import io
from models import User, EntireTree, TreeRoot, TreeBranch, TreeLeap, TreeStem, TreeSize
from db_connect import db

from model_init import model_dict

def getClassfication(model_file_name):
    if model_dict[model_file_name] is not None:
        model = tf.keras.models.load_model('./model/classification/'+model_file_name+'.h5') #모델 로드
    else:
        model = model_dict[model_file_name]
    return model

#detection function
def detection(binaryimg):
    resultlist = []
    
    encoded_img = np.fromstring(binaryimg, dtype = np.uint8)
    img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    
    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #이미지를 읽고 rgb로 변환한다. (opencv는 bgr로 읽음)
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.uint8)[tf.newaxis, ...] #텐서 형식으로 변환
    

    height = img_array.shape[0]
    width = img_array.shape[1]

    draw_img = img_array.copy()

    #모델 로드
    # model = tf.saved_model.load('.\model\detection\saved_model')
    ### 전역변수로 해보기 추가 ###
    if model_dict["detection"] is not None:
        model = tf.saved_model.load('.\model\detection\saved_model')
    else:
        model = model_dict["detection"]
    ############################

    #사용자 이미지 추론 (detection)
    result = model(img_tensor)
    result = {key:value.numpy() for key,value in result.items()}
    
    #임계값 지정. 50% 이상일 때만 바운딩박스 그림
    SCORE_THRESHOLD = 0.5
    OBJECT_DEFAULT_COUNT = 4 #클래스 개수

    #클래스 매칭
    labels_to_names = {1.0:'1001', 2.0:'1002', 3.0:'1003', 4.0:'1004'}
    
    # 선언
    tree_height = 0
    tree_width = 0
    
    stem_height = 0
    stem_width = 0

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
        
        # 1001: 가지, 잎
        # 1002: 줄기
        # 1003: 뿌리
        # 1004: 나무 전체

        ###########추가
        if labels_to_names[class_id] == '1004':
            tree_height = bottom-top
            tree_width = right-left
            # tree_size, location = tree_size_loc(height, width, top, bottom, left, right)
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

#classification funcation
def classification(model_file_name, binary_img, SIZE):###########수정 내용. 매개변수 SIZE 추가. 이유: 모델 네트워크가 모두 같지 않다면 인풋 사이즈가 달라짐
    # model_file_name: str
    # img: np array
    # 예시: 나무 타입 분류

    # model = tf.keras.models.load_model('./model/classification/'+model_file_name+'.h5') #모델 로드
    ### 전역변수로 해보기 추가 ###
    model = getClassfication(model_file_name)
    ############################

    encoded_img = np.fromstring(binary_img, dtype = np.uint8)
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    img_array = cv2.cvtColor(decoded_img, cv2.COLOR_BGR2RGB) #아까 잘라서 저장한 나무 전체 이미지 불러온다
    image = cv2.resize(img_array, dsize=(SIZE, SIZE)) #리사이징
    image = np.array(image) #np array type으로 변경
    image = image/255.
    image = np.expand_dims(image, axis=0) #차원 추가
   
    prediction = model.predict(image) #추론
    result = np.argmax(prediction) #결과 확인.
    return result

#######멀티라벨 모델로 갈 경우 사용.
def classification_multi(model_file_name, binary_img, class_li, SIZE, COUNT):

    SCORE_THRESHOLD = 0.1

    # model = tf.keras.models.load_model('./model/classification/'+model_file_name+'.h5') #모델 로드
    ### 전역변수로 해보기 추가 ###
    model = getClassfication(model_file_name)
    ############################

    encoded_img = np.fromstring(binary_img, dtype = np.uint8)
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    img_array = cv2.cvtColor(decoded_img, cv2.COLOR_BGR2RGB) #아까 잘라서 저장한 나무 전체 이미지 불러온다
    image = cv2.resize(img_array, dsize=(SIZE, SIZE)) #리사이징
    image = np.array(image) #np array type으로 변경
    image = np.expand_dims(image, axis=0) #차원 추가

    proba = model.predict(image)

    sorted_categories = np.argsort(proba[0])[:-(COUNT+1):-1]

    resultlist=[]

    for i in range(COUNT):
     if proba[0][sorted_categories[i]] > SCORE_THRESHOLD:
        resultlist.append(class_li[sorted_categories[i]])
        print(class_li[sorted_categories[i]])
        print('score:', proba[0][sorted_categories[i]])
    return resultlist

def cropimgToDB(class_id, npbinary):
    userid = session['userid']
    print("session: " + userid)
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
    else: 
        if class_id == 1.0:
            user.crop2_1001 = npbinary
        elif class_id == 2.0:
            user.crop2_1002 = npbinary
        elif class_id == 3.0:
            user.crop2_1003 = npbinary
        else: # class_id == 4.0
            user.crop2_1004 = npbinary
    db.session.commit()
