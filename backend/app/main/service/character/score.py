"""
index
0 - 공격성/온화함
1 - 사회불안/자신감
2 - 우울/행복
3 - 대인회피/사회성
4 - 낮은 자존감/높은 자존감
"""
# size
SCORE_TREE_SIZE_SMALL = [0, 0, 1, 1, 1]

# location
SCORE_TREE_LOCATION_LEFT = [0, 0, 0, 1, 0]
SCORE_TREE_LOCATION_CENTER = [0, 0, 0, 0, 0]
SCORE_TREE_LOCATION_RIGHT = [1, 1, 0, 0, 0]

# stem
SCORE_TREE_STEM_LONG = [1, 1, 0, 0, 0]
SCORE_TREE_STEM_SHORT = [0, 0, 1, 1, 1]
SCORE_TREE_STEM_SLIM = [0, 0, 1, 0, 1]
SCORE_TREE_STEM_THICK = [1, 1, 0, 0, 0]
SCORE_TREE_STEM_RING = [1, 1, 1, 1, 0]
SCORE_TREE_STEM_ANIMAL = [0, 1, 1, 0, 1]

# leaf, fruit
SCORE_TREE_LEAF_BIG = [0, 0, 1, 1, 1]
SCORE_TREE_LEAF_LEAFY = [1, 0, 0, 0, 0]
SCORE_TREE_LEAF_FLOWER = [1, 1, 0, 0, 0]
SCORE_TREE_LEAF_FRUIT = [1, 1, 0, 0, 0]

# branch
SCORE_TREE_BRANCH_NET = [0, 0, 0, 0, 0]
SCORE_TREE_BRANCH_UP = [1, 0, 0, 1, 0]

# root
SCORE_TREE_ROOT_XRAY = [0, 1, 0, 0, 0]
SCORE_TREE_ROOT_ABOVE = [0, 1, 0, 0, 1]
SCORE_TREE_ROOT_HIGHLIGHT = [1, 1, 0, 1, 0]

# tree type
SCORE_TREE_TYPE = [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 1], [0, 0, 1, 1, 0], [0, 1, 0, 0, 0]]