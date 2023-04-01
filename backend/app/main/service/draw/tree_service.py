# standard library imports
import io
# Third party imports
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image

# local application imports
from main.service.draw.common import *
from main.model.domain.user.user_model import *
from main.model.domain.result.house_model import * 
from main.model.domain.result.tree_model import * 
from main.model.repository.user.user_repository import *
from main.service.draw.common import *

class UserTreeResult:
    size = ''
    type = ''
    leap = ''
    branch = ''
    stem = ''
    root = ''

    def __init__(self):
        pass

def call_tree_model(userid):
    user = find_user(userid=userid)
    img_binary = user.treeimg
    
    result = UserTreeResult()

    # 0. tree_size_location
    size_result_list = detection_tree(img_binary, userid)
    size_result_str = result_match(TreeSize, size_result_list)
    result.size = size_result_str

    # 1. tree_type 나무 전체 => 0 1 2 3 4 중에 하나 
    if user.tree1004 is not None:
        type_result_list=[]
        type_result_list.append(classification('tree_type', user.tree1004, 300))
        type_result_str = result_match(EntireTree, type_result_list)
        result.type = type_result_str

    # 2. 3. 잎, 열매, 꽃, 가지
    if user.tree1001 is not None:
        label_names = ['열매있음','윗쪽으로 뻗는','잎이 안 큰','잎무성한','꽃있음', '그물', '잎이 큰']
        label_return = classification_multi('leaf_branch', user.tree1001, label_names, 200, 7)
        leap_result_list = []
        if '열매있음' in label_return:
            leap_result_list.append(3)
        if '잎무성한' in label_return:
            leap_result_list.append(1)
        if '잎이 큰' in label_return:
            leap_result_list.append(0)
        if '꽃있음' in label_return:
            leap_result_list.append(2)
        leap_result_str = result_match(TreeLeap, leap_result_list)
        result.leap = leap_result_str
    
        branch_result_list=[]
        if '윗쪽으로 뻗는' in label_return:
            branch_result_list.append(1)
        if '그물' in label_return:
            branch_result_list.append(0)
        branch_result_str = result_match(TreeBranch, branch_result_list)
        result.branch = branch_result_str

    # 4. stem 줄기 => [0, 0, 0]
    if user.tree1002 is not None:
        label_names = ['나이테_나무껍질_옹이_O','동물_곤충_O','나이테_나무껍질_옹이_X']
        stem_result_list = []
        label_return = classification_multi('stem', user.tree1002, label_names, 200, 3)

        if '나이테_나무껍질_옹이_O' in label_return:
            stem_result_list.append(0)
        if '동물_곤충_O' in label_return:
            stem_result_list.append(1)
        
        stem_result_str = result_match(TreeStem, stem_result_list)
        result.stem = stem_result_str

    # 5. root 뿌리 => 1 2 3 4 5 중에 하나
    if user.tree1003 is not None:
        root_result_list = []
        root_result_list.append(classification('root', user.tree1003, 150))
        root_result_str = result_match(TreeRoot, root_result_list)
        result.root = root_result_str

    save_user_tree(userid=userid, result=result)

#detection function
def detection_tree(img_binary, userid):
    result_list = []
    
    encoded_img = np.fromstring(img_binary, dtype = np.uint8)
    decoded_img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
    
    img_array = cv2.cvtColor(decoded_img, cv2.COLOR_BGR2RGB) #이미지를 읽고 rgb로 변환한다. (opencv는 bgr로 읽음)
    img_tensor = tf.convert_to_tensor(img_array, dtype=tf.uint8)[tf.newaxis, ...] #텐서 형식으로 변환
    
    height = img_array.shape[0]
    width = img_array.shape[1]

    draw_img = img_array.copy()

    model = get_detection_model('saved_model')

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
            result_list.extend(tree_size_loc(height, width, top, bottom, left, right))
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
        update_user_tree_crop(class_id, userid ,img_byte_arr)
        # cv2.imwrite('./image/'+labels_to_names[class_id]+'.png',cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)) #크롭하여 로컬에 저장 (저장 안 하는 방식으로 수정?)

        print('class_id', class_id)

        caption = "{}: {:.4f}".format(labels_to_names[class_id], score)
        print(caption)  #score 콘솔에서 확인
    
    ################
    # 줄기 사이즈
    # stem_size = 0 #보통이다
    if stem_height > tree_height * (1/2):
        # stem_size = 2 #길다
        result_list.append(4)
    elif stem_height < tree_height * (1/6):
        stem_size = 1  #짧다
        result_list.append(5)

    # 줄기 굵기
    stem_thickness = 0 #보통이다
    if stem_width  < tree_width/10:
        stem_thickness = 1 # 얇다
        result_list.append(7)
    elif stem_width > tree_width * 0.4: # 0.4로 수정함
        stem_thickness = 2 # 굵다
        result_list.append(6)
    ##########    
    return result_list


def tree_size_loc(height, width, top, bottom, left, right):##새로 생성
  treesizeResult = []
  img_size = height*width
  tree_size = (bottom-top)*(right-left) #트리 크기
  img_center = width / 2 ##그림 중앙 좌표
  tree_center = left + ((right-left)/2) #트리 중앙 좌표

  if tree_size < img_size / 4:
    treesizeResult.append(0)

  if tree_center < img_center / 2:
    treesizeResult.append(1)
  elif tree_center > img_center * 1.5:
     treesizeResult.append(3)
  else:
     treesizeResult.append(2)
       
  return treesizeResult