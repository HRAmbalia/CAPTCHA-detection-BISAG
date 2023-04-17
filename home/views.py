### THIS VIEW DISPLAYS DETAILS ABOUT PRETRAINED MODEL FOR TEXT CAPTCHA & IT'LL DISPALY SEPARATE CAPTCHA IMAGES AND WILL PREDICT CAPCTHA FOR THIS IMAGES

#######################################################################################################

from django.shortcuts import render

# Create your views here.
import os
import random
import base64
import json
import re
import importlib
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from xml.dom.minidom import parseString

#######################################################################################################

XML_FILE_PATH = '/home/hr/Documents/BISAG/Code/Project_TCGD/final_Proj/home/static/data.xml'

#######################################################################################################

def index(request):
    context = {}
    return render(request, 'index.html', context)

#######################################################################################################

def selectModel(request):
    data = {}

    # Counting total number of model available
    file = open(XML_FILE_PATH,'r')
    dat = file.read()
    file.close()
    dom = parseString(dat)
    model_count = len(dom.getElementsByTagName('model-path'))
    
    # Getting options for Drop-down list
    my_options = [{'value': '', 'label': 'Please select an option'}]
    for i in range(1, model_count+1):
        my_options += ([{'value': 'model' + str(i), 'label': 'Model ' + str(i)}])
    print(my_options)

    # Fetchig all the data of model, collecting it into variable my_list_json
    for i in range(1, model_count+1):
        print("Iteration : " + str(i))
        fetched_data = fetchDataFromXML(i)
        data.update(fetched_data)
    my_list_json = json.dumps(data)

    # Returning page
    context = {'my_list_json': my_list_json}
    print(context)
    context.update({'my_options': my_options})
    return render(request, 'selectModel.html', context)

#######################################################################################################

def fetchDataFromXML(id):
    dict = {}
    num = str(id)

    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()

    # Getting CAPTCHA path
    CAPTCHA_PATH = root.find("./m" + num + "/captcha-path").text
    files = os.listdir(CAPTCHA_PATH)
    files = [f for f in files if os.path.isfile(os.path.join(CAPTCHA_PATH, f))]
    random_file = random.choice(files)
    random_image_path = CAPTCHA_PATH + random_file
    strValue = re.sub(".*static/", '', random_image_path )
    print(strValue)
    dict.update({'captcha_filepath_M'+num:strValue})

    # Find the m element and get the image element under it
    M_ELEMENT = root.find('.//m' + num)
    IMAGE_ELEMENT = M_ELEMENT.find('.//image')

    ACCURACY_FILEPATH_ELEMENT = IMAGE_ELEMENT.find('.//accurecy/filename')
    accurecy_filepath_value = ACCURACY_FILEPATH_ELEMENT.text
    dict.update({'accurecy_filepath_M'+num:accurecy_filepath_value})

    LOSS_FILEPATH_ELEMENT = IMAGE_ELEMENT.find('.//loss/filename')
    loss_filepath_value = LOSS_FILEPATH_ELEMENT.text
    dict.update({'loss_filepath_M'+num:loss_filepath_value})

    OVERALLACCURACY_ELEMENT = root.find('.//m' + num + '/overallaccurecy')
    overallaccurecy_value = OVERALLACCURACY_ELEMENT.text
    dict.update({'overallaccurecy_M'+num:overallaccurecy_value})

    OVERALLLOSS_ELEMENT = root.find('.//m' + num + '/overallloss')
    overallloss_value = OVERALLLOSS_ELEMENT.text
    dict.update({'overallloss_M'+num:overallloss_value})

    CODEPATH_ELEMENT = root.find('.//m' + num + '/trained-code-path')
    codepath_value = CODEPATH_ELEMENT.text
    new_s = codepath_value.split("home")[-1]
    
    dict.update({'code_M'+num:new_s})

    return dict

#######################################################################################################

def textCaptcha(request, selected_option):
    context = {}
    # from selected_option fetch model number like 1, 2 or 3
    context.update({'modelNumber': selected_option})
    modelId = ""
    for char in selected_option:
        if char.isdigit() or char == '.':
            modelId += char

    # Add random Image to context
    random_image_path = generateTextCaptcha(modelId)
    with open(random_image_path, 'rb') as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
    context.update({'image': encoded_image})

    # Getting true CAPTCHA value
    filename = os.path.basename(random_image_path)
    print("filename : " + filename)
    if "_" in filename:
        originatText = filename.split("_")[0]
    elif "." in filename:
        originatText = filename.split(".")[0]
    context.update({'originatText': originatText})

    # Add Predicted CAPTCHA to Context
    predicted_text = recognizeTextCaptcha(random_image_path, modelId)
    context.update({'predictedText': predicted_text})

    # Adding Model Details
    context = addModelDetails(context, modelId)

    # Returning page
    return render(request, 'textCaptcha.html', context)

#######################################################################################################

def addModelDetails(cont, modelId):
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()

    DESCRIPTION_ELEMENT = root.find('.//m' + modelId + '/descreption')
    description_value = DESCRIPTION_ELEMENT.text
    cont.update({'description':description_value})

    OVERALLACCURACY_ELEMENT = root.find('.//m' + modelId + '/overallaccurecy')
    overallaccurecy_value = OVERALLACCURACY_ELEMENT.text
    cont.update({'overallaccurecy':overallaccurecy_value})

    OVERALLLOSS_ELEMENT = root.find('.//m' + modelId + '/overallloss')
    overallloss_value = OVERALLLOSS_ELEMENT.text
    cont.update({'overallloss':overallloss_value})

    MODEL_EXPLAINED_ELEMENT = root.find('.//m' + modelId + '/model-explained')
    modelexplained_value = MODEL_EXPLAINED_ELEMENT.text
    cont.update({'modelexplained':modelexplained_value})

    CAPTCHA_WIDTH_ELEMENT = root.find('.//m' + modelId + '/captcha-image-width')
    captchawidth_value = CAPTCHA_WIDTH_ELEMENT.text
    cont.update({'captchawidth':captchawidth_value})

    CAPTCHA_HEIGHT_ELEMENT = root.find('.//m' + modelId + '/captcha-image-height')
    captchaheight_value = CAPTCHA_HEIGHT_ELEMENT.text
    cont.update({'captchaheight':captchaheight_value})

    CHARACTERS_IN_CAPTCHA_ELEMENT = root.find('.//m' + modelId + '/characters-in-captcha')
    characterincaptcha_value = CHARACTERS_IN_CAPTCHA_ELEMENT.text
    cont.update({'characterincaptcha':characterincaptcha_value})

    M_ELEMENT = root.find('.//m' + modelId)
    MODELIMAGE_ELEMENT = M_ELEMENT.find('.//image')
    MODEL_FILEPATH_ELEMENT = MODELIMAGE_ELEMENT.find('.//model/filename')
    model_filepath_value = MODEL_FILEPATH_ELEMENT.text
    cont.update({'model_filepath_value':model_filepath_value})

    return cont

#######################################################################################################

# According to model number Randomly selects file from folder
def generateTextCaptcha(modelId):
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    CAPTCHA_PATH = root.find("./m" + modelId + "/captcha-path").text
    files = os.listdir(CAPTCHA_PATH)
    files = [f for f in files if os.path.isfile(os.path.join(CAPTCHA_PATH, f))]
    random_file = random.choice(files)
    random_image_path = CAPTCHA_PATH + random_file
    return random_image_path

#######################################################################################################

def recognizeTextCaptcha(random_image_path, modelId):
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    PYTHON_FILE_PATH = root.find("./m" + modelId + "/predict-file").text
    print(PYTHON_FILE_PATH)
    #
    python_file_name = re.sub(".*predictProg/", '', PYTHON_FILE_PATH )
    module_name = python_file_name.replace(".py", "")
    #
    try:
        spec = importlib.util.spec_from_file_location(module_name, PYTHON_FILE_PATH)
        my_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(my_module)
        print("random_image_path : " + random_image_path)
        print("modelId : " + modelId)
    except ImportError as e:
        return HttpResponse(f"Error: {e}")
    predicted_captcha = my_module.predict(random_image_path, modelId)
    return predicted_captcha

#######################################################################################################
