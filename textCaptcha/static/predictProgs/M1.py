import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image as im
import numpy as np # linear algebra
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from keras.models import load_model

XML_FILE_PATH = '/home/hr/Documents/BISAG/Code/Project_TCGD/final_Proj/textCaptcha/static/data.xml'

def predict(filepath, modelId):
    # print("Hello from M3.py")

    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    MODEL_PATH = root.find("./model" + str(modelId) + "/model-path").text
    model = load_model(MODEL_PATH)

    H, W, C = 100, 120, 3  # height, width, 3(RGB channels)
    img = image.load_img(filepath)#, target_size=(H, W))
    img = image.load_img(filepath, target_size=(H, W))
    x_1 = image.img_to_array(img) / 255.0
    x_1 = np.expand_dims(x_1, axis=0)

    y_pred_1 = model.predict(x_1)

    predicted_labels_1 = [chr(int(i)) for i in np.argmax(y_pred_1, axis=-1)[0]]
    predicted_label = ''.join(predicted_labels_1)
    
    # print(predicted_label)
    return predicted_label