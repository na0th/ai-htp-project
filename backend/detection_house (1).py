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

    detection_list = []###############추가

    roof_width_list = [] ######추가
    wall_list = []
    window_list = []
    door_list = []


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

        # detection_list.append(labels_to_names[class_id]) #탐지 오브젝트 리스트에담는다
        

        if labels_to_names[class_id] == '1001':
          roof_width = right-left
          roof_width_list.append(roof_width)

        elif labels_to_names[class_id] == '1002':
          wall_left = left
          wall_right = right
          wall_height = bottom - top
          wall_width = right-left

          wall_list.append([wall_left, wall_right, wall_height, wall_width])

        elif labels_to_names[class_id] == '1003':
          window_height = bottom - top
          window_width = right - left
          window_list.append([window_height, window_width])
          # detection_list_1003.append(labels_to_names[class_id])
        elif labels_to_names[class_id] == '1004':
          door_left = left
          door_right = right
          door_height = bottom - top
          door_width = right - left

          door_list.append([door_left, door_right, door_height, door_width])
        
        detection_list.append(labels_to_names[class_id]) ##########추가. 모든 탐지 오브젝트를 담는다.


        print('class_id', class_id)

        caption = "{}: {:.4f}".format(labels_to_names[class_id], score)
        print(caption)  #score 콘솔에서 확인    
    
    door_edge = 0
    window_cnt = 0
    if detection_list.count('1002') == 1 and detection_list.count('1004') == 1: #문, 벽이 한 개라면
      door_edge = door_edge(door_width, wall_width, door_left, door_right, wall_left, wall_right) #가장자리 함수
    if detection_list.count('1003') >= 2: ##창문 2개 이상
      window_cnt = 1

    #큰 지붕
    if detection_list.count('1001') == 1 and detection_list.count('1002') == 1: #지붕 벽 각각 하나
      roof_size = roof_size(roof_width, wall_width)
    elif detection_list.count('1001') >= 2 or detection_list.count('1002') >= 2: #지붕이나 벽이 2개 이상
      wall_width_list = []
      wall_cnt = detection_list.count('1002')
      
      for i in range(0, wall_cnt):
        wall_width_list.append(wall_list[i][3])
      
      roof_size = roof_size(max(roof_width_list), max(wall_width_list))
    elif detection_list.count('1001') == 0: #지붕 없다
      pass
    #큰 문 작은 문
    if detection_list.count('1004') == 1 and detection_list.count('1002') == 1:
      door_size = door_size(door_height, door_width, wall_height, wall_width)
    elif detection_list.count('1004') > 2 and detection_list.count('1002') == 1:




    
