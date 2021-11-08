from django.shortcuts  import render,redirect
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http.response import JsonResponse

import jwt
curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL 
jwt_key = settings.JWT_SECURITY_KEY
jwt_algo = 'HS256'
from . import models
import time

def getTimeStamp():
    [t1,t2] = str(time.time()).split(".")
    return t1+t2

def createJWTToken(data):
    return jwt.encode(data,jwt_key,jwt_algo)
def decodeJWTToken(data):
    return jwt.decode(token, jwt_key, algorithms=[jwt_algo])
def home(request):
    # if 'email' in request.COOKIES :
    #     return redirect(curl+'myuser/')
    # elif 'adminMail' in request.COOKIES:
    #     return redirect(curl + 'myadmin/')
    # elif 'dpId' in request.COOKIES:
    #     return redirect(curl + 'dp/')
    # else:
    #     query = "select * from catagory"
    #     models.cursor.execute(query)
    #     clist = models.cursor.fetchall()
    response=render(request, "base.html",{'curl': curl, 'media_url': media_url})
    return response

def login(request):
    if request.method=='GET':
        response=render(request, "login.html",{'curl': curl, 'media_url': media_url})
        return response
    elif request.method=='POST':
        email=request.POST.get('email')
        password = request.POST.get('password')
        query="select * from user where email='%s' and password='%s' "%(email,password)
        models.cursor.execute(query)
        user=models.cursor.fetchall()
        print(user)
        if len(user)>0:
            response=JsonResponse({"data":user[0]})
            new_token = createJWTToken({"email":email,"password":password})
            response.set_cookie("token",new_token)
            return response
        else:
            return JsonResponse({"error":"Invalid Credentials...."})
    else:
        return JsonResponse({"otp":1,'email':''})

def signup(request):
    if request.method=='GET':
        response=render(request, "signup.html",{'curl': curl, 'media_url': media_url})
        print(response)
        return response
    elif request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        user_id = "user"+getTimeStamp()
        query = "insert into user (name,user_id,email,mobile,password,status,createdAt) values('%s','%s','%s','%s','%s','%s','%s')" % (name,user_id,email,mobile,password,0,getTimeStamp())
        models.cursor.execute(query)
        models.db.commit()
        # user=models.cursor.fetchall()
        # if len(user)>0:
        #     response=redirect(curl+"myuser/")
        #     new_token = createJWTToken(email)
        #     response.set_cookie("token",new_token)
        #     return response
        # else:
        #     return redirect(curl)
        return JsonResponse({"otp":1,'email':''})
    else:
        return JsonResponse({"otp":1,'email':''})
    
def flatType(request):
    response=render(request, "flatType.html",{'curl': curl, 'media_url': media_url})
    return response
def rooms(request):
    response=render(request, "rooms.html",{'curl': curl, 'media_url': media_url})
    return response