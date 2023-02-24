# 1001: 지붕
# 1002: 벽
# 1003: 창문
# 1004: 문

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
      door_size = 1 #넓은
    else:
      door_size = 2 #큰 (길이)
  elif door_height < wall_height*(1/5):
    if door_width < wall_width*(1/4):
      door_size = 3 #작은
    else:
      door_size = 4 #낮은 (길이)
  return door_size

#문 가장자리 함수
def door_edge(door_width, wall_width, door_left, door_right, wall_left, wall_right):
  door_edge = 0 #치우치지 않은
  if door_left <= wall_left+(wall_width*(1/4)):
    if door_right <=wall_left+(wall_widht*(1/2)):
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
