import json

from django.forms import forms, fields
from django.http import HttpResponse
from django.shortcuts import render, redirect
import hashlib
from Login import models
from Login.models import Images, User

import requests
import base64
from PIL import Image


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            try:
                user = models.User.objects.get(ID=username)
            except:
                return HttpResponse("user_not_exists")
            if user.password == password:
                return HttpResponse("login_success")
            else:
                return HttpResponse("wrong_password")
    if request.method == "GET":
        return render(request, 'login.html')


def javaLogin(request, username, password):
    username = str(username)
    password = str(password)
    if request.method == "GET":
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            try:
                user = models.User.objects.get(ID=username)
            except:
                return HttpResponse("user_not_exists")
            if user.password == password:
                return HttpResponse("login_success")
            else:
                return HttpResponse("wrong_password")
    if request.method == "GET":
        return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


class UploadForm(forms.Form):
    user = fields.CharField()
    img = fields.FileField()


def upload(request):
    obj = UploadForm(request.POST, request.FILES)
    if obj.is_valid():
        user = obj.cleaned_data['user']
        image = obj.cleaned_data['img']
        print(user)
        print(image.name)
        print(image.size)
        f = open(image.name, 'wb+')
        # chunks表示一块块的
        for line in image.chunks():
            f.write(line)
        f.close()

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

        f = open(image.name, 'rb')
        img = base64.b64encode(f.read())

        params = {"image": str(img, 'utf-8'), "image_type": 'BASE64', "face_field": 'expression', "max_face_num": 5}

        # params = "{\"image\":str(img,'utf-8')\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"face_field\":\"faceshape,facetype\"}"
        access_token = '24.725fe4567d475a9293d00a2576e11489.2592000.1578904189.282335-17855989'
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/json'}
        response = requests.post(request_url, data=params, headers=headers)

        if response:
            dict = response.json()
            expression = dict.get('result').get('face_list')[0].get('expression').get('type')
            left = dict.get('result').get('face_list')[0].get('location').get('left')
            top = dict.get('result').get('face_list')[0].get('location').get('top')
            width = dict.get('result').get('face_list')[0].get('location').get('width')
            height = dict.get('result').get('face_list')[0].get('location').get('height')

            face = Image.open(image.name)
            face.convert("RGBA")
            box = (int(left), int(top), int(left + width), int(top + height))
            emoji = Image.open('./images/emoji_happy.png')
            emoji.convert('RGBA')
            emoji = emoji.resize((box[2] - box[0], box[3] - box[1]))
            face.paste(emoji, box, emoji)
            face.save('./result.png')

        return HttpResponse('upload success')


# 云盘实现
def cloud_upload(request, owner):
    obj = UploadForm(request.POST, request.FILES)
    upload_img = request.FILES.get('img')
    img_name = upload_img.name
    f = open("./images/cloud/" + img_name + "_" + owner + ".png", 'wb')
    for line in upload_img.chunks():
        f.write(line)
    f.close()
    owner_o = User.objects.get(ID=owner)
    Images.objects.create(filename=img_name, user=owner_o)
    owner = User.objects.get(ID=owner)
    images = Images.objects.filter(user=owner)
    info = images
    for i in images:
        i.filename = "/static/cloud/" + i.filename + "_1.png"
    return render(request, 'cloud.html', locals())


def cloud(request, owner):
    owner = User.objects.get(ID=owner)
    images = Images.objects.filter(user=owner)
    info = images
    for i in images:
        i.filename = "/static/cloud/" + i.filename + "_1.png"
    return render(request, 'cloud.html', locals())


def a_cloud(request, owner):
    owner = User.objects.get(ID=owner)
    images = Images.objects.filter(user=owner)
    dict_f = {}
    count = 1
    for i in images:
        i.filename = "/static/cloud/" + i.filename + "_1.png"
        dict_f[count] = "http://212.64.48.72" + i.filename
        count = count + 1
    print(dict_f)
    j = json.dumps(dict_f)
    return HttpResponse(j)


# 演示实现
def demonstrate(request):
    return render(request, 'demonstrate.html')


def detect(request):
    obj = UploadForm(request.POST, request.FILES)
    upload_img = request.FILES.get('img')
    f = open("./images/demonstrate/t.png", 'wb')
    for line in upload_img.chunks():
        f.write(line)
    f.close()
    # 上传完成
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    f = open("./images/demonstrate/t.png", 'rb')
    img = base64.b64encode(f.read())
    params = {"image": str(img, 'utf-8'), "image_type": 'BASE64', "face_field": 'expression', "max_face_num": 5}
    # params = "{\"image\":str(img,'utf-8')\"027d8308a2ec665acb1bdf63e513bcb9\",\"image_type\":\"FACE_TOKEN\",\"face_field\":\"faceshape,facetype\"}"
    access_token = '24.725fe4567d475a9293d00a2576e11489.2592000.1578904189.282335-17855989'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        dict = response.json()
        expression = dict.get('result').get('face_list')[0].get('expression').get('type')
        left = dict.get('result').get('face_list')[0].get('location').get('left')
        top = dict.get('result').get('face_list')[0].get('location').get('top')
        width = dict.get('result').get('face_list')[0].get('location').get('width')
        height = dict.get('result').get('face_list')[0].get('location').get('height')

        face = Image.open("./images/demonstrate/t.png")
        face.convert("RGBA")
        box = (int(left), int(top), int(left + width), int(top + height))
        if expression=='smile':
            emoji = Image.open('./images/emoji_happy.png')
        else:
            emoji = Image.open('./images/emoji_none.png')
        emoji.convert('RGBA')
        emoji = emoji.resize((box[2] - box[0], box[3] - box[1]))
        face.paste(emoji, box, emoji)
        face.save('./images/demonstrate/result.png')
    return render(request, 'demonstrated.html', locals())


def test(request, username):
    psw = User.objects.get(ID=username).password
    return HttpResponse(psw)
