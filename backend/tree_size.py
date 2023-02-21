
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