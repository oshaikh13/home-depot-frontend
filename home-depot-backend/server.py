"""
visualize results for test image
"""

import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import operator
from torch.autograd import Variable

import transforms as transforms
from skimage import io, util
from skimage.transform import resize
from models import *

from flask import Flask, request, jsonify, abort, safe_join, send_file
from flask_cors import CORS

import base64
import re

from scipy import stats

class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

app = Flask(__name__)
CORS(app)

@app.route('/compare', methods=['POST'])
def compare():
    if request.method == 'POST':

        body = request.get_json()

        print(body['id'])

        if (not 'img' in body): abort(400)
        
        filename_usermimic = safe_join("images/usermimic/", str(body["id"]) + ".jpg")
        filename_mimic = safe_join("images/mimic/", str(body["id"]) + ".jpg")

        if not os.path.isfile(filename_mimic): 
            abort(404)

        removed_header = re.sub(r"^data:image\/[a-zA-Z]+;base64,", "", body["img"])

        with open(filename_usermimic, "wb") as fh:
            fh.write(base64.b64decode(removed_header))
            print(filename_usermimic)
        
        
        #jsonify(getEmotionScore("images/mimic/" + str(body["id"]) + ".jpg"))
        scores = {}
        scores["mimic"] = getEmotionScore(filename_mimic, False)
        scores["user_mimic"] = getEmotionScore(filename_usermimic, False)

        print(body["id"])
        print(scores["user_mimic"])

        x = []
        y = []

        for class_name in class_names:
            x.append(scores["mimic"][class_name])
            y.append(scores["user_mimic"][class_name])

        scores["r"] = stats.pearsonr(x, y)

        return jsonify(scores)

@app.route('/getmimic/<int:file_id>', methods=['get'])
def get_mimic(file_id):
    if request.method == 'GET':
        filename = safe_join("images/mimic/", str(file_id) + ".jpg")
        if not os.path.isfile(filename): 
            abort(404)
        return send_file(filename, mimetype='image/jpg')


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def cropND(img, bounding):
    start = tuple(map(lambda a, da: a//2-da//2, img.shape, bounding))
    end = tuple(map(operator.add, start, bounding))
    slices = tuple(map(slice, start, end))
    return img[slices]

def getEmotionScore(imageDirectory, resizeImg):
    cut_size = 44

    transform_test = transforms.Compose([
        transforms.TenCrop(cut_size),
        transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
    ])

    raw_img = io.imread(imageDirectory)
    
    if resizeImg == True: 
        raw_img = cropND(raw_img, (400, 400))

    io.imsave("screenshot.jpg", raw_img)

    gray = rgb2gray(raw_img)
    gray = resize(gray, (48,48), mode='symmetric').astype(np.uint8)

    img = gray[:, :, np.newaxis]

    img = np.concatenate((img, img, img), axis=2)
    img = Image.fromarray(img)
    inputs = transform_test(img)

    net = VGG('VGG19')
    checkpoint = torch.load(os.path.join('FER2013_VGG19', 'PrivateTest_model.t7'))
    net.load_state_dict(checkpoint['net'])
    net.cuda()
    net.eval()

    ncrops, c, h, w = np.shape(inputs)

    inputs = inputs.view(-1, c, h, w)
    inputs = inputs.cuda()
    inputs = Variable(inputs, volatile=True)
    outputs = net(inputs)

    outputs_avg = outputs.view(ncrops, -1).mean(0)  # avg over crops

    score = F.softmax(outputs_avg)
    _, predicted = torch.max(outputs_avg.data, 0)
    
    scoreDict = {}

    for i in range(len(class_names)):
        scoreDict[class_names[i]] = float(score.data.cpu().numpy()[i])
        
    scoreDict["expression"] = str(class_names[int(predicted.cpu().numpy())])   
    return scoreDict

# for i in range(1, 11):
#     print(i)
#     print(getEmotionScore("images/mimic/" + str(i) + ".jpg", False))



