from flask import session, g

#tf.keras lib
from tensorflow import keras
from keras.models import Model

import tensorflow as tf
import numpy as np

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
    if model_dict[model_file_name] is None:
        model = tf.keras.models.load_model('./model/classification/'+model_file_name+'.h5') #모델 로드
    else:
        model = model_dict[model_file_name]
    return model

def getDetection(model_file_name):
    if model_dict[model_file_name] is None:
        model = tf.saved_model.load('.\model\detection\\'+model_file_name) #모델 로드
    else: 
        model = model_dict[model_file_name]
    return model

#detection function
def detection_tree(binaryimg):
    resultlist = []
    
    encoded_img = np.fromstring(binaryimg, dtype = np.uint8)
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    
    img_array = cv2.cvtColor(decoded_img, cv2.COLOR_BGR2RGB) #이미지를 읽고 rgb로 변환한다. (opencv는 bgr로 읽음)
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.uint8)[tf.newaxis, ...] #텐서 형식으로 변환
    

    height = img_array.shape[0]
    width = img_array.shape[1]

    draw_img = img_array.copy()

    #모델 로드
    # model = tf.saved_model.load('.\model\detection\saved_model')
    ### 전역변수로 해보기 추가 ###
    # if model_dict["detection"] is not None:
    #     model = tf.saved_model.load('.\model\detection\saved_model')
    # else:
    #     model = model_dict["detection"]
    model = getDetection('saved_model')
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
        # print(i)
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
    elif stem_width > tree_width * 0.4: # 0.4로 수정함
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

    SCORE_THRESHOLD = 0.3

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

    # print("********************************")
    # print(proba)
    # print(sorted_categories)
    # print(len(class_li))
    # print(class_li)
    # print("********************************")

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

def detection_house(binaryimg):
    roofresult=[]
    doorresult=[]
    windowresult=[]
    wall_width_list=[]

    encoded_img = np.fromstring(binaryimg, dtype = np.uint8)
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)

    img_array = cv2.cvtColor(decoded_img, cv2.COLOR_BGR2RGB) #이미지를 읽고 rgb로 변환한다. (opencv는 bgr로 읽음)
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.uint8)[tf.newaxis, ...] #텐서 형식으로 변환
    
    height = img_array.shape[0]
    width = img_array.shape[1]

    draw_img = img_array.copy()

    #모델 로드
    model = getDetection('saved_model2')

    #사용자 이미지 추론 (detection)
    result = model(img_tensor)
    result = {key:value.numpy() for key,value in result.items()}
    
    #임계값 지정. 50% 이상일 때만 바운딩박스 그림
    SCORE_THRESHOLD = 0.5
    OBJECT_DEFAULT_COUNT = 4 #클래스 개수

    #클래스 매칭
    labels_to_names = {1.0:'1001', 2.0:'1002', 3.0:'1003', 4.0:'1004'}
    
    detection_list = [] ###############추가
 
    ######추가
    roof_width_list = [] 
    
    wall_list = []
    wall_width_list=[]
    wall_height_list=[]

    window_list = [] 
    window_width_list = []
    window_height_list = []

    door_list = []
    door_width_list=[]
    door_height_list=[]
    
    # 1001: 지붕
    # 1002: 벽
    # 1003: 창문
    # 1004: 문

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
        
        if labels_to_names[class_id] == '1001':
          roof_width = right-left
          roof_width_list.append(roof_width)

        elif labels_to_names[class_id] == '1002':
          wall_left = left
          wall_right = right
          wall_height = bottom - top
          wall_width = right-left
          wall_width_list.append(wall_width)
          wall_height_list.append(wall_height)
          wall_list.append([wall_left, wall_right, wall_height, wall_width])

        elif labels_to_names[class_id] == '1003':
          window_height = bottom - top
          window_width = right - left
          window_width_list.append(window_width)
          window_height_list.append(window_height)
          window_list.append([window_height, window_width])
          
        elif labels_to_names[class_id] == '1004':
          door_left = left
          door_right = right
          door_height = bottom - top
          door_width = right - left
          door_list.append([door_left, door_right, door_height, door_width])
          door_width_list.append(door_width)
          door_height_list.append(door_height)
        
        detection_list.append(labels_to_names[class_id]) ##########추가. 모든 탐지 오브젝트를 담는다.

        # print('class_id', class_id)

        caption = "{}: {:.4f}".format(labels_to_names[class_id], score)
        # print(caption)  #score 콘솔에서 확인    
    
    if detection_list.count('1002') == 1 and detection_list.count('1004') == 1: #문, 벽이 한 개라면
        door_edge_result = door_edge(door_width, wall_width, door_left, door_right, wall_left, wall_right)
        if door_edge_result == 1 or door_edge_result == 2:
            doorresult.append(5) #가장자리 함수
    
    if detection_list.count('1003') >= 2: ##창문 2개 이상
        windowresult.append(1)
    elif detection_list.count('1003') == 0:
        windowresult.append(0)
    
    #큰 지붕
    if detection_list.count('1001') == 1 and detection_list.count('1002') == 1: #지붕 벽 각각 하나
       if roof_size(roof_width, wall_width) == 1: # 지붕이 있는데 크다.
          roofresult.append(1)
    elif detection_list.count('1001') == 0: #지붕 없다
        roofresult.append(0)

    #지붕이나 벽이 2개 이상
    if (detection_list.count('1001') >= 2 and detection_list.count('1002') >= 1) or (detection_list.count('1001') >= 1 and detection_list.count('1002') >= 2): 
        roofresult.append(roof_size(max(roof_width_list), max(wall_width_list)))

    # 창문이 한 개라도 있으면
    if detection_list.count('1003') >= 1 and detection_list.count('1002') >= 1:
        #창문 크기
        window_size_result = window_size(max(window_height_list), max(window_width_list), max(wall_height_list), max(wall_width_list))
        if window_size_result == 1:
           window_list.append(3)
        elif window_size_result == 2:
           window_list.append(2)
        # window_height, window_width, wall_height, wall_width

    # 큰 문 작은 문 판별
    # 문이 한 개고 벽이 한 개이면
    # if detection_list.count('1004') == 1 and detection_list.count('1002') == 1:
    #     door_size_result = door_size(door_height, door_width, wall_height, wall_width)
    #     if door_size_result != 0:
    #         doorresult.append(door_size_result)
    # # 문이 두 개 이상이고 벽이 한 개 이상이면
    # elif detection_list.count('1004') > 1 and detection_list.count('1002') == 1:
    #     door_size_result = door_size(max(door_height_list), max(door_width_list), max(wall_height_list), max(wall_width_list))
    #     if door_size_result != 0:
    #         doorresult.append(door_size_result)

    # print(roofresult)
    # print(doorresult)
    # print(windowresult)

    print("지붕 개수: ", detection_list.count('1001'))
    print("벽 개수: ", detection_list.count('1002'))
    print("창문 개수: ", detection_list.count('1003'))
    print("문 개수: ", detection_list.count('1004'))

    print(detection_list)

    return {
        "roofresult": roofresult,
        "doorresult": doorresult,
        "windowresult": windowresult,
    }

#지붕이 큰가? 함수
def roof_size(roof_width, wall_width):
  roof_size = 0
  if int(roof_width) > int(wall_width)*3:
    roof_size = 1 #크다
  return roof_size

#문이 큰가? 함수
def door_size(door_height, door_width, wall_height, wall_width):
  door_size = 0 #보통
  if door_height > wall_height*(4/5):
    if door_width > wall_width*(3/5):
      door_size = 2 #넓은
    else:
      door_size = 1 #큰 (길이)
  elif door_height < wall_height*(1/5):
    if door_width < wall_width*(1/4):
      door_size = 4 #작은
    else:
      door_size = 3 #낮은 (길이)
  return door_size

#문 가장자리 함수
def door_edge(door_width, wall_width, door_left, door_right, wall_left, wall_right):
  door_edge = 0 #치우치지 않은
  if door_left <= wall_left+(wall_width*(1/4)):
    if door_right <=wall_left+(wall_width*(1/2)):
      door_edge = 1 #왼쪽 가장자리로 치우친
  elif door_left >= wall_left+(wall_width / 2):
    if door_right >= wall_right - (wall_width/4):
      door_edght = 2 #오른쪽 가장자리로 치우친
  return door_edge

#창문 크기 함수
def window_size(window_height, window_width, wall_height, wall_width):
  window_size = 0 #보통
  if window_width < wall_width/6:
    window_size = 1 # 좁은. 작다.
  elif window_width >= wall_width/2:
    if window_height >= wall_height*0.8:
      window_size = 2 #큰 창문 (통유리창 정도)
  return window_size

