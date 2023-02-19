from flask import Blueprint, request, g, session, jsonify
from db_connect import db
import base64
from flask_cors import CORS
from models import User

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
        # 세션 구현 해야함
        params = request.get_json()
        session['username'] = params['userName']
        # print(params['username'])

        # insert
        user = User(username=params['userName'])
        db.session.add(user)
        db.session.commit()

        # version 1: token
        # token = jwt.encode({'userid' : user.userid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=100)})
        # return jsonify({'token': token })
    
        # version 2: 
        return jsonify({'message': 'The username is saved.', "userid": user.userid }), 200

        # version 3:
        # return jsonify(
		# 	result = "success",
		# 	# 검증된 경우, access 토큰 반환
		# 	access_token = create_access_token(identity = user.userid,
		# 									expires_delta = False)
		# )

        # version 4
        # resp = make_response()
        # resp.set_cookie('userid', str(user.userid))
        # return resp
    
def callModel(imgdata):
    detection('./image/test_3.PNG') #경로에서 불러온 이미지를 request 메시지에서 받은 이미지로 변경할 것
    result = classification('tree_type', './image/1004.png')
    return result

@bp.route('/tree/', methods=['POST', 'GET'])
def showFirst():
    # if g.user == None:
    #     return redirect(url_for('views.showMain'))
    if request.method == 'POST':
        params = request.get_json()
        userid = params['userid']
        if userid == None:
            return 404
        
        str = params['image'][22:]
        # print(str)

        imgdata = base64.b64decode(str)
        # filename = 'receivedimage.jpg'  # I assume you have a way of picking unique filenames
        # with open(filename, 'wb') as f:
        #     f.write(imgdata)

        # picture = convertToBinaryData(filename)      

        # 모델 넣을 자리
        resultText = callModel(imgdata)

        # user = User.query.filter_by(userid).first()
        user = db.session.query(User).filter(User.userid == userid).first()
        user.image1 = str
        user.result1 = resultText
        db.session.commit()

        return jsonify({'message': 'The image is saved.'}), 200

@bp.route('/home/', methods=['POST', 'GET'])
def showSecond():
    # if g.user == None:
    #     return redirect(url_for('views.showMain'))
    if request.method == 'POST':
        params = request.get_json()
        userid = params['userid']
        if userid == None:
            return 404

        str = params['image'][22:]
        # print(params['image'])

        imgdata = base64.b64decode(str)
        filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

        picture = convertToBinaryData(filename) # 이미지를 binary로 변환하여 db에 저장하였다.

        # 모델 넣을 자리
        resultText = 'great!'

        user = db.session.query(User).filter(User.userid == userid).first()
        user.image2 = picture
        user.result2 = resultText
        db.session.commit()

        return jsonify({'message': 'The image is saved.'}), 200



@bp.route('/result/', methods=['POST', 'GET'])
def showThird():
    # if g.user == None:
    #     return redirect(url_for('views.showMain'))
    if request.method == 'GET':
        params = request.get_json()
        userid = params['userid']
        if userid == None:
            return 404

        user = db.session.query(User).filter(User.userid == userid).first()

        str_base641 = base64.b64encode(user.image1)
        base64_str1 = str_base641.decode('utf-8')

        str_base642 = base64.b64encode(user.image2)
        base64_str2 = str_base642.decode('utf-8')

        # version 1
        # response = {
        #     "username": user.username,
        #     "image1": base64_str1,
        #     "image2": base64_str2,
        #     "result1": user.result1,
        #     "result2": user.result2
        # }

        # version 1
        return jsonify({
            "username": user.username,
            "image1": base64_str1,
            "image2": base64_str2,
            "result1": user.result1,
            "result2": user.result2
        }), 200

        # version 2
        # return json.dumps(response)

        # version 3
        # return render_template("forth.html", username=g.user.username, image1=g.user.image1, image2=g.user.image2, result1=g.user.result1, result2=g.user.result2)

        # 혹은 response에 담아서 보내는 방식도 있음.
        # redirect(location, statuscode, response)

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
        cv2.imwrite('./image/'+labels_to_names[class_id]+'.png',cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)) #크롭하여 로컬에 저장 (저장 안 하는 방식으로 수정?)

        print('class_id', class_id)

        caption = "{}: {:.4f}".format(labels_to_names[class_id], score)
        print(caption)  #score 콘솔에서 확인

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