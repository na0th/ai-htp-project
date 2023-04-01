import tensorflow as tf
#efficient lib
from efficientnet.keras import EfficientNetB3
from keras.models import Model
#tf.keras lib
from tensorflow import keras

# 전역 변수
model_dict = {
        "saved_model": tf.saved_model.load('ai_model/detection/saved_model'),
        "saved_model2": tf.saved_model.load('ai_model/detection/saved_model2'),
        "leaf_branch": tf.keras.models.load_model('ai_model/classification/leaf_branch.h5'),
        "tree_type": tf.keras.models.load_model('ai_model/classification/tree_type.h5'),
        "root": tf.keras.models.load_model('ai_model/classification/root.h5'),
        "stem": tf.keras.models.load_model('ai_model/classification/stem.h5'),
        "house": tf.keras.models.load_model('ai_model/classification/house.h5'),
    }
