import cv2
import string
import numpy as np 
import xml.etree.ElementTree as ET
from keras.models import load_model
from tensorflow.keras.preprocessing import image 

XML_FILE_PATH = '/home/hr/Documents/BISAG/Code/Project_TCGD/final_Proj/home/static/data.xml'

def predict(filepath, modelId):
    print("Hello from M2.py")

    # Gets MODEL_PATH for given modelId 
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    MODEL_PATH = root.find("./m" + str(modelId) + "/model-path").text
    model = load_model(MODEL_PATH)

    img = image.load_img(filepath, target_size=(100, 120))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    y_pred = model.predict(x)
    predicted_labels = [chr(int(i)) for i in np.argmax(y_pred, axis=-1)[0]]
    predicted_labels = ''.join(predicted_labels)
    return predicted_labels