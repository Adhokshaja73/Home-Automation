
from operator import itemgetter
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Device, HomeBoardTopic
from allauth.account.decorators import login_required   

import paho.mqtt.client as paho
import re
import fuzzywuzzy.fuzz as fuzz

from .forms import *
import cv2
import numpy as np
import face_recognition
from base64 import b64decode
import os
from .identifier import *
# Create your views here

identifier = Identifier()

@login_required
def home(request):
    if(request.method == "POST"):
        # Save the post data
        topic = request.POST['topic']
        if(HomeBoardTopic.objects.filter(topic = topic).exists()):
            return(JsonResponse({'status' : 'failed' , 'err_msg' : 'Topic Already Subscribed. Please check your OWN board for topic.'}))
        user = request.user
        newHomeBoard = HomeBoardTopic( topic = topic, user = user)
        newHomeBoard.save()
        return(JsonResponse({'status' : 'success'}))
    else:
        currentUserHome = HomeBoardTopic.objects.filter(user = request.user)
        if(currentUserHome.exists()):
            currentUserHome = currentUserHome.get()
            if(Device.objects.filter(topic = currentUserHome.topic).exists()):
                return(redirect("home.html"))
            else:
                return(redirect("add_device.html"))
        else:
            return(render(request, "registration.html"))


@login_required
def addDevice(request):
    if(request.method == "POST"):
        # save data
        deviceName = request.POST["deviceName"]
        pinNum = request.POST["pinNum"]
        topic = HomeBoardTopic.objects.filter(user = request.user).get().topic
        if(Device.objects.filter(topic = topic).filter(deviceName = deviceName).exists()):
            return(JsonResponse({"status" : "fail", "err_msg" : "Device with same name already exists"}))
        elif(Device.objects.filter(topic = topic).filter(pinNum = pinNum).exists()):
            return(JsonResponse({"status" : "fail", "err_msg" : "Another device is connected to the same pin."}))
        newDevice = Device(topic = topic, deviceName = deviceName, pinNum = pinNum)
        newDevice.save()
        return(JsonResponse({"status" : "success"}))
    else:
        return(render(request, "add_device.html"))

@login_required
def removeDevice(request):
    if(request.method == "POST"):
        # save data
        deviceName = request.POST["deviceName"]
        topic = HomeBoardTopic.objects.filter(user = request.user).get().topic
        device = Device.objects.filter(topic = topic).filter(deviceName = deviceName)
        if(device.exists()):
            device.delete()
            return(JsonResponse({"status" : "success"}))
        else:
            return(JsonResponse({"status" : "failure", "err_msg"  : "device " + deviceName + " does not exist"}))
    else:
        return(render(request, "remove_device.html"))


# MQTT FUNCTIONS
def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def publishMessage(topic, pinNum, val):
    broker="10.5.15.103"
    port=1883
    client1= paho.Client("control1")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port) 
    message = pinNum * 10 + val
    ret = client1.publish(topic, message)
    if(ret):
        return("success")
    else:
        return("failed to publish message")


@login_required
def main(request):
    if(not UserImages.objects.filter(user = request.user).exists()):
        return(redirect("add_image.html"))
    if(request.method == "POST"):
        topic = HomeBoardTopic.objects.filter(user = request.user).get().topic
        message = request.POST["message"]
        print(message)

        deviceList = Device.objects.filter(topic = topic)
        devices = []

        # Using fuzzywuzzy to match input command with all 
        # device names
        # improve this with NLP
        for i in deviceList:
            devices.append(i.deviceName)
        re.sub('[^A-Za-z0-9 ]+', '', message)
        message = message.lower()
        if("door" in message):
            if("unlock" in message):
                return(redirect("unlock_door.html"))
            elif("lock" in message):
                publishMessage(topic, 28, 0)
                return(JsonResponse({"status" : "Door locked"}))
        flag = False
        turnOnRatio = {}
        turnOffRatio = {}
        for i in deviceList:
            turnOnRatio[i.deviceName] = fuzz.ratio("turn on " + i.deviceName, message)
            turnOffRatio[i.deviceName] = fuzz.ratio("turn off " + i.deviceName, message)

        turnOnRatio = sorted(turnOnRatio.items(), key=lambda kv: kv[1])
        turnOffRatio = sorted(turnOffRatio.items(), key=lambda kv:kv[1])
        
        turnOffRatio.reverse()
        turnOnRatio.reverse()
        
        print(turnOffRatio, turnOnRatio)
        value = 1
        status = "on"
        deviceName = turnOnRatio[0][0]
        ratio = turnOnRatio[0][1]
        if(turnOffRatio[0][1]  > turnOnRatio[0][1]):
            value = 0
            status = "off"
            deviceName = turnOffRatio[0][0]
            ratio = turnOffRatio[0][1]
        print(ratio)
        if(ratio < 95):
            return(JsonResponse({"status" : "Device Does not exist"}))
        else:
            pinNum = deviceList.filter(deviceName = deviceName).get().pinNum
            publishMessage(topic, pinNum, value)
            return(JsonResponse({"status" : "Turned "+ status +" "+ deviceName}))    
    else:
        return(render(request, "main.html"))

@login_required
def addNewImage(request):
    if(request.method == "POST"):
        data_uri = request.POST["img"]
        header, encoded = data_uri.split(",", 1)
        data = b64decode(encoded)
        imagePath = os.path.join(os.getcwd(), "media/images/known_people/" + request.user.username + ".jpg" )
        with open(imagePath, "wb") as f:
            f.write(data)  
        retVal = identifier.refresh()
        if(retVal == 1):
            userImage = UserImages.objects.create(user = request.user , image = "images/known_people/" + request.user.username + ".jpg")
            userImage.save()
            return(JsonResponse({"status" : "success"})) 
        else:
            return(JsonResponse({"status" : "failed"}))
    if(UserImages.objects.filter(user = request.user).exists()):
        return(redirect("/")) 
    else:
        return render(request, 'add_image.html')

@login_required
def unlockDoor(request):
    if(request.method == "POST"):
        data_uri = request.POST["img"]
        header, encoded = data_uri.split(",", 1)
        data = b64decode(encoded)
        jpg_as_np = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        names = identifier.check(img)
        if(request.user.username in names):
            print("TURN ON SERVO TO UNLOCK")
            topic = HomeBoardTopic.objects.filter(user = request.user).get().topic
            publishMessage(topic, 28, 1)
            return(JsonResponse({"status" : "Door Unlocked"}))
        else:
            print("Wrong face")
            return(JsonResponse({"status" : "UnAuthorized Person"}))
    else:
        return(render(request,"unlock_door.html"))