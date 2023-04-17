### THIS PAGE WILL GENERATE TEXT CAPTCHA IMAGE AND WILL PREDICT CAPTCHA USING UPI OR OUR TRAINED MODEL

#######################################################################################################

from django.shortcuts import render

# Create your views here.
import io
import os
import re
import json
import base64
import random
import string
import importlib
import http.client
import cloudinary.uploader
import cloudinary.api
import xml.etree.ElementTree as ET
from captcha.image import ImageCaptcha
from django.http import HttpResponse
from django.core.files.storage import default_storage
from cloudinary.utils import cloudinary_url
#

#######################################################################################################

XML_FILE_PATH = "/home/hr/Documents/BISAG/Code/Project_TCGD/final_Proj/textCaptcha/static/data.xml"

#######################################################################################################

def generateCaptcha(request):
    context = {}
    if request.method == 'POST':
        captchaText = request.POST.get('input')
        rndm = request.POST.get('rndm')
        if rndm == 'on':
            captchaText = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        filenm = captchaText + '.png'
        
        # Create captcha image
        captcha_image = ImageCaptcha(width=120, height=100)
        img_bytes = io.BytesIO()
        captcha_image.write(captchaText, img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Create HTTP response with image as content
        response = HttpResponse(img_bytes, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=' + filenm
        return response
    return render(request, 'generateCaptcha.html', context)

#######################################################################################################

def fetchData(data):
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    value = root.find(".//"+data).text
    return value

#######################################################################################################

def getLink(file_path):
    cloudinary.config(
        cloud_name = fetchData('cloud-name'),
        api_key = fetchData('api-key'),
        api_secret = fetchData('api-secret')
    )
    result = cloudinary.uploader.upload(file_path)
    image_url, _ = cloudinary_url(result['public_id'], format=result['format'], crop='fill', width=300, height=300)
    return image_url

#######################################################################################################

def fetchCaptchaText(image_url):
    # Fetch all keys
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    key_elements = root.findall('.//X-RapidAPI-Key/*')
    key_list = [element.text for element in key_elements]

    headers_template = {
        'X-RapidAPI-Key': '',
        'X-RapidAPI-Host': fetchData('X-RapidAPI-Host')
    }
    conn = http.client.HTTPSConnection(fetchData('HTTPSConnection-client'))
    for key in key_list:
        headers = headers_template.copy()
        headers['X-RapidAPI-Key'] = key
        conn.request("GET", '/solve?image=' + image_url, headers=headers)
        res = conn.getresponse()
        data = res.read()
        response = data.decode("utf-8")
        if 'captcha' in response:
            response_json = json.loads(response)
            captcha_value = response_json['captcha']
            return captcha_value

#######################################################################################################

def deleteImagefromWebsite(image_url):
    cloudinary.config(
        cloud_name = fetchData('cloud-name'),
        api_key = fetchData('api-key'),
        api_secret = fetchData('api-secret')
    )
    image_url = image_url
    public_id_match = re.search(r'upload/(.*?)/', image_url)
    if public_id_match:
        public_id = public_id_match.group(1)
    else:
        print("Error: could not extract public ID from image URL.")
    cloudinary.api.delete_resources([public_id])
    print("Image deleted successfully.")

#######################################################################################################

def deleteImagefromOS(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    except OSError as e:
        print(f"Error deleting {file_path}: {e.strerror}")

#######################################################################################################

def recognizeTextCaptcha_usingModel(random_image_path, modelId):
    tree = ET.parse(XML_FILE_PATH)
    root = tree.getroot()
    PYTHON_FILE_PATH = root.find("./model" + modelId + "/predict-file").text
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
        print (HttpResponse(f"Error: {e}"))
    predicted_captcha = my_module.predict(random_image_path, modelId)
    return predicted_captcha

#######################################################################################################

def recognizeTextCaptcha_usingAPI(file_path):
    # Upload image and get image link
    image_link = getLink(file_path)
    # Sending this link to CAPTCHA api to get data
    # 'https://rapidapi.com/metropolisapi/api/captcha'
    captcha_value = fetchCaptchaText(image_link)
    if not bool(captcha_value.strip()):
        captcha_value = "try later"
    deleteImagefromWebsite(image_link)
    return captcha_value
    
#######################################################################################################

def recognizeCaptcha(request):
    context = {}
    if request.method == 'POST':
        # Get the uploaded image from the request and saves it
        selected_option = request.POST.get('opt')
        uploaded_image = request.FILES['image']
        file_path = default_storage.save('./textCaptcha/static/' + uploaded_image.name, uploaded_image)

        print("selected_option : " + selected_option)

        ### METHOD 01 : USING OUR TRAINED MODEL
        if (selected_option=="Model"):
            captcha_value = recognizeTextCaptcha_usingModel(file_path, str(1))
            print("captcha_value_Model : " + captcha_value)
            context.update({'captcha_value':captcha_value})
        
        ### METHOD 02 : USING API
        elif (selected_option=="API"):
            captcha_value = recognizeTextCaptcha_usingAPI(file_path)
            print("captcha_value_API : " + captcha_value)
            context.update({'captcha_value':captcha_value})

        # Adding image to context
        with open(file_path, 'rb') as f:
            binary_data = f.read()
        image_data = base64.b64encode(binary_data).decode("ascii")
        context.update({'image_data': image_data})

        deleteImagefromOS(file_path)

    return render(request, 'recognizeCaptcha.html', context)

#######################################################################################################
