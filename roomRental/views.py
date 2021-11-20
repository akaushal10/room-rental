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
    return jwt.decode(data, jwt_key, algorithms=[jwt_algo])
class Guest:
    def __init__(self):
        print("contructor")
        self.isLogin = 4
        self.token = False
        self.adminToken = False
    def home(self,request):
        if self.token:
            return redirect(curl+'myuser/')
        else:
            roomQuery = "select * from room_types limit 3"
            models.cursor.execute(roomQuery)
            roomsList = models.cursor.fetchall()
            if 'token' in request.COOKIES:
                token = request.COOKIES["token"]
                data = decodeJWTToken(token)
                query="select * from user where email='%s' and password='%s' "%(data["email"],data["password"])
                models.cursor.execute(query)
                user=models.cursor.fetchall()
                if len(user)>0:
                    self.user = user[0]
                    response = redirect(curl+'myuser/')
                else:
                    response=render(request, "home.html",{'curl': curl, 'media_url': media_url,"rooms":roomsList})
                return response
            elif 'adminToken' in request.COOKIES:
                adminToken = request.COOKIES["adminToken"]
                data = decodeJWTToken(adminToken)
                query="select * from admins where admin_id='%s' and admin_password='%s' "%(data["email"],data["password"])
                models.cursor.execute(query)
                admin=models.cursor.fetchall()
                if len(admin)>0:
                    response = redirect(curl+'myadmin/')
                else:
                    response=render(request, "home.html",{'curl': curl, 'media_url': media_url,"rooms":roomsList})
                return response
            else:
                response=render(request, "home.html",{'curl': curl, 'media_url': media_url,"rooms":roomsList})
                return response
    def adminLogin(self,request):
        if request.method=='GET':
            if self.adminToken:
                return redirect(curl+"myadmin/")
            else:
                if 'adminToken' in request.COOKIES:
                    return redirect(curl+"myadmin")
                else:
                    response=render(request, "adminLogin.html",{'curl': curl, 'media_url': media_url})
                    return response
        elif request.method=='POST':
            email=request.POST.get('email')
            password = request.POST.get('password')
            query="select * from admins where admin_id='%s' and admin_password='%s' "%(email,password)
            models.cursor.execute(query)
            user=models.cursor.fetchall()
            if len(user)>0:
                response=JsonResponse({"data":user[0],"curl":curl})
                new_token = createJWTToken({"email":email,"password":password})
                response.set_cookie("adminToken",new_token)
                return response
            else:
                return JsonResponse({"error":"Invalid Credentials...."})
        else:
            return JsonResponse({"otp":1,'email':''})
        
    def login(self,request):
        if request.method=='GET':
            if self.token:
                return redirect(curl+"myuser/")
            else:
                if 'token' in request.COOKIES:
                    return redirect(curl)
                else:
                    response=render(request, "login.html",{'curl': curl, 'media_url': media_url})
                    return response
        elif request.method=='POST':
            email=request.POST.get('email')
            password = request.POST.get('password')
            query="select * from user where email='%s' and password='%s' "%(email,password)
            models.cursor.execute(query)
            user=models.cursor.fetchall()
            if len(user)>0:
                response=JsonResponse({"data":user[0],"curl":curl})
                new_token = createJWTToken({"email":email,"password":password})
                response.set_cookie("token",new_token)
                return response
            else:
                return JsonResponse({"error":"Invalid Credentials...."})
        else:
            return JsonResponse({"otp":1,'email':''})

    def signup(self,request):
        if request.method=='GET':
            if self.token:
                return redirect(curl+"myuser/")
            else:
                if 'token' in request.COOKIES:
                    return redirect(curl)
                else:
                    response=render(request, "signup.html",{'curl': curl, 'media_url': media_url})
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
            return JsonResponse({"success":1,"message":"User Created Succesfull...!","curl":curl})
        else:
            return JsonResponse({"otp":1,'email':''})
        
    def flatType(self,request):
        if self.token:
            response= redirect(curl+"myuser/flatType")
        else:
            if 'token' in request.COOKIES:
                response= redirect(curl+"myuser/flatType")
            else:
                getFlatQuery = "select * from flat_types"
                models.cursor.execute(getFlatQuery)
                flats = models.cursor.fetchall()
                response=render(request, "flatType.html",{'curl': curl, 'media_url': media_url,"flats":flats})
        return response
    def about(self,request):
        if self.token:
            response= redirect(curl+"myuser/about")
        else:
            if 'token' in request.COOKIES:
                response= redirect(curl+"myuser/about")
            else:
                response=render(request, "about.html",{'curl': curl, 'media_url': media_url,})
        return response
    def help(self,request):
        if self.token:
            response= redirect(curl+"myuser/help")
        else:
            if 'token' in request.COOKIES:
                response= redirect(curl+"myuser/help")
            else:
                getHelpQuery = "select * from helps"
                models.cursor.execute(getHelpQuery)
                helps = models.cursor.fetchall()
                response=render(request, "help.html",{'curl': curl, 'media_url': media_url,"helps":helps})
        return response

    def rooms(self,request):
        flatId = request.GET.get('flatId')
        if self.token:
            response= redirect(curl+"myuser/flatType")
        else:
            if 'token' in request.COOKIES:
                response= redirect(curl+"myuser/flatType")
            else:
                getFlatName = "select flat_name from flat_types where flat_id = '%s'"%(flatId)
                models.cursor.execute(getFlatName)
                flatName = models.cursor.fetchall()[0][0]
                getRoomsQuery = "select * from room_types where flat_id='%s'"%(flatId)
                models.cursor.execute(getRoomsQuery)
                rooms = models.cursor.fetchall()
                response=render(request, "rooms.html",{'curl': curl, 'media_url': media_url,"rooms":rooms,"flatName":flatName})
        return response