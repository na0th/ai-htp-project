resultStr2 = {} # 결과 dic

def save_result(table, findId): # db테이블과 찾고자하는 id 값 받고 resultStr에 저장
    resultData = db.session.query(table).filter(table.id == findId).first()
    if resultData.result is not None:
        resultStr[resultData.subtitle] = resultData.result
    return 

## 지붕 모델
# roof_rlabel 결과라벨 => [0,0] 형식 출력, [지붕o, 지붕 크다]
roof_rlabel = [0,0]
for i in range(0,len(roof_rlabel)):
    if roof_rlabel[i] == 1:
        save_result(HouseRoof, i)

## 문 모델
# door_rlabel 결과라벨 => [0,0] 형식 출력, [문o, 문 크기]
door_rlabel = [0,0]
if door_rlabel[0] == 1:
    save_result(HouseDoor, 0)
if door_rlabel[0] == 1:
    save_result(HouseDoor, 1)
else:
    save_result(HouseDoor, 2)

## 창 모델
# window_rlabel 결과라벨 => [0,0,0] 형식 출력, [창 개수, 큰 창o, 작은 창o]
window_rlabel = [0,0,0]
if window_rlabel[0] == 0: #창x
    save_result(HouseWindow, 0)
elif window_rlabel[0] >= 2: #창 2개 이상
    save_result(HouseWindow, 1)

if window_rlabel[1] == 1:
    save_result(HouseWindow, 2)
if window_rlabel[2] == 1:
    save_result(HouseWindow, 3)