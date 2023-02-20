# flask_server.py

#flask lib
import numpy as np
import tensorflow as tf
from flask import Flask

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

#detection function
def detection(img):
    
    img_array = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB) #이미지를 읽고 rgb로 변환한다. (opencv는 bgr로 읽음)
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.uint8)[tf.newaxis, ...] #텐서 형식으로 변환
    

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
        
        ###########추가
        if labels_to_names[class_id] == '1004':
            tree_height = bottom-top
            tree_width = right-left
            tree_size, location = tree_size_loc(height, width, top, bottom, left, right)
            print('location',location)
        elif labels_to_names[class_id] == '1002':
            stem_height = bottom-top
            stem_width = right-left
        ###########

        cv2.imwrite('./image/'+labels_to_names[class_id]+'.png',cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)) #크롭하여 로컬에 저장 (저장 안 하는 방식으로 수정?)

        print('class_id', class_id)

        caption = "{}: {:.4f}".format(labels_to_names[class_id], score)
        print(caption)  #score 콘솔에서 확인
    
    ################
    stem_size = 0 #보통이다
    if stem_height > tree_height * (1/2):
        stem_size = 2 #길다
    elif stem_height < tree_height * (1/6):
        stem_size = 1  #짧다

    stem_thickness = 0 #보통이다
    if stem_width  < tree_width/10:
        stem_thickness = 1 #얇다
    elif stem_width > tree_width * 0.23:
        stem_thickness = 2 #굵다

    ##########    
    
#classification funcation
def classification(model_file_name, img_path):
    #예시: 나무 타입 분류
    treeType_model = tf.keras.models.load_model('./model/classification/'+model_file_name+'.h5') #모델 로드

    img_array = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB) #아까 잘라서 저장한 나무 전체 이미지 불러온다
    image = cv2.resize(img_array, dsize=(300, 300)) #리사이징
    test_image = np.array(image) #np array type으로 변경
    test_image = np.expand_dims(test_image, axis=0) #차원 추가
    test_image.shape #shape확인

    prediction = treeType_model.predict(test_image) #추론
    tree_type = np.argmax(prediction) #결과 확인. 0: 상록수
    return str(tree_type)

def tree_size_loc(height, width, top, bottom, left, right):##새로 생성
  img_size = height*width
  tree_size = (bottom-top)*(right-left) #트리 크기
  img_center = width / 2 #그림 중앙 좌표
  tree_center = left + ((right-left)/2) #트리 중앙 좌표

  tree_size_flag = 0 #보통, 크다

  if tree_size < img_size / 4:
    tree_size_flag = 1 #작다

  if tree_center < img_center / 2:
    tree_location = 0 #left
  elif tree_center > img_center * 1.5:
    tree_location = 2 #right
  else:
    tree_location = 1 #center
  return tree_size_flag, tree_location





app = Flask(__name__)

@app.route('/')
def home():
    return 'This is home!'


@app.route('/predict', methods=['POST'])
def predict():

    detection('./image/test_3.PNG') #경로에서 불러온 이미지를 request 메시지에서 받은 이미지로 변경할 것
    result = classification('tree_type', './image/1004.png')

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2431, threaded=False)