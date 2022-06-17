from email import message
from http.server import HTTPServer
import imp
from multiprocessing import reduction
from os import stat
from pickletools import read_uint1
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import Device, HomeBoardTopic
from allauth.account.decorators import login_required   

import paho.mqtt.client as paho

# Create your views here

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

    


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def publishMessage(topic, pinNum, val):
    broker="localhost"
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
    if(request.method == "POST"):
        topic = HomeBoardTopic.objects.filter(user = request.user).get().topic
        '''
            TODO IMPORTANT  
            process the message using NLP
        '''
        message = request.POST["message"]
        words = message.split("_")
        try:
            deviceName = words[0]
            status = words[1]
        except:
            return(JsonResponse({'status' : 'fail', 'err_msg' : 'invalid message format.'}))
        val = 0
        if(status == "on"):
            val = 1
        elif(status == "off"):
            val = 0
        else:
            return(JsonResponse({ 'status' : 'failed' , 'err_msg' : 'status can only be on or off'}))
        device = Device.objects.filter(topic = topic).filter(deviceName = deviceName)
        if(device.exists()):
            pinNum = device.get().pinNum
            ret = publishMessage(topic, pinNum, val)
            return(JsonResponse({'status' : ret}))
        else:
            return(JsonResponse({'status' : "failed", "err_msg" : "device does not exist"}))
    else:
        return(render(request, "main.html"))



