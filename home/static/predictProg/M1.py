import cv2
import numpy as np 
import xml.etree.ElementTree as ET
from keras.models import load_model

XML_FILE_PATH = '/home/hr/Documents/BISAG/Code/Project_TCGD/final_Proj/home/static/data.xml'

def predict(filepath, modelId):
    print("Hello from M1.py")

    # Gets MODEL_PATH for given modelId 
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    MODEL_PATH = root.find("./m" + str(modelId) + "/model-path").text
    model = load_model(MODEL_PATH)
    character = root.find("./m" + str(modelId) + "/possible-characters").text
    
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

    if img is not None: #image foud at file path
        img = img / 255.0 #Scale image
    else:
        return("Not detected")

    res = np.array(model.predict(img[np.newaxis, :, :, np.newaxis])) #np.newaxis=1 
    #added this bcoz x_train 970*50*200*1
    #returns array of size 1*5*36 
    result = np.reshape(res, (5, 36)) #reshape the array
    k_ind = []
    for i in result:
        k_ind.append(np.argmax(i)) #adds the index of the char found in captcha

    capt = '' #string to store predicted captcha
    for k in k_ind:
        capt += character[k] #finds the char corresponding to the index
    print("capt from M1 : " + capt)

    return (capt)

