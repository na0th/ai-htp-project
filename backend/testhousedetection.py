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

import base64
from model_predict import *

print("시작")

detection_house2("test_house.jpg")
