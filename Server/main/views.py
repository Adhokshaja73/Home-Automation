from http.server import HTTPServer
import imp
from multiprocessing import reduction
from pickletools import read_uint1
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import HomeBoardTopic
from allauth.account.decorators import login_required   

import paho.mqtt.client as paho

# Create your views here

@login_required
def home(request):
    if(request.method == "POST"):
        # Save the post data
        topic = request.POST['topic']
        if(HomeBoardTopic.objects.filter(topic = topic).exists()):
            return(render(request,"registration.html", {'err_msg' : 'Topic Already Subscribed. Please check your OWN board for topic.'}))
        user = request.user
        newHomeBoard = HomeBoardTopic( topic = topic, user = user)
        newHomeBoard.save()
        return(redirect("/"))
    else:
        currentUserHome = HomeBoardTopic.objects.filter(user = request.user)
        if(currentUserHome.exists()):
            currentUserHome = currentUserHome.get()
            return(render(request, "index.html", { 'board' : currentUserHome}))
        else:
            return(render(request, "registration.html"))


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def postMessage(request, message):
    broker="localhost"
    port=1883
    client1= paho.Client("control1")                           #create client object
    client1.on_publish = on_publish                          #assign function to callback
    client1.connect(broker,port)  
    topic = HomeBoardTopic.objects.filter(user = request.user).get().topic
    ret= client1.publish(topic, message)
    return(JsonResponse({'Success' : 'ok'}))