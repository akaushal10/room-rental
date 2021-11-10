from django.shortcuts import render,redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.core.files.storage import FileSystemStorage
from roomRental import models
from datetime import datetime
import time
import jwt

curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL 
jwt_key = settings.JWT_SECURITY_KEY
jwt_algo = 'HS256'
def getTimeStamp():
    [t1,t2] = str(time.time()).split(".")
    return t1+t2

def createJWTToken(data):
    return jwt.encode(data,jwt_key,jwt_algo)
def decodeJWTToken(data):
    return jwt.decode(data, jwt_key, algorithms=[jwt_algo])

class User:
    def __init__(self):
        self.token = False
    def userHome(self,request):
        if self.token:
            response=render(request, "userHome.html",{'curl': curl, 'media_url': media_url,"user":self.user,"isLogin":True})
            return response
        else:
            if 'token' in request.COOKIES:
                token = request.COOKIES["token"]
                data = decodeJWTToken(token)
                query="select * from user where email='%s' and password='%s' "%(data["email"],data["password"])
                models.cursor.execute(query)
                user=models.cursor.fetchall()
                if len(user)>0:
                    self.user = user[0]
                    response=render(request, "user/userHome.html",{'curl': curl, 'media_url': media_url,"user":self.user,"isLogin":True})
                else:
                    response= redirect(curl)
                return response
            else:
                response= redirect(curl)
                return response
    def flatType(self,request):
        getFlatQuery = "select * from flat_types"
        models.cursor.execute(getFlatQuery)
        flats = models.cursor.fetchall()
        if self.token:
            response=render(request, "flatType.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"flats":flats})
        else:
            if 'token' in request.COOKIES:
                self.token = request.COOKIES["token"]
                response=render(request, "flatType.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"flats":flats})
            else:
                response= redirect(curl+"flatType/")
        return response

    def rooms(self,request):
        flatId = request.GET.get('flatId')
        getRoomsQuery = "select * from room_types where flat_id='%s'"%(flatId)
        models.cursor.execute(getRoomsQuery)
        rooms = models.cursor.fetchall()
        if self.token:
            response=render(request, "rooms.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"rooms":rooms})
        else:
            if 'token' in request.COOKIES:
                self.token = request.COOKIES["token"]
                response=render(request, "rooms.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"rooms":rooms})
            else:
                response= redirect(curl+"flatType/")
        return response
    def bookRoom(self,request):
        if request.method=='GET':
            room_id = request.GET.get('roomId') 
            data = decodeJWTToken(request.COOKIES["token"])

            getUserQuery="select user_id from user where email='%s' and password='%s' "%(data["email"],data["password"])
            models.cursor.execute(getUserQuery)
            userData=models.cursor.fetchall()[0]

            getRoomQuery="select * from room_types where room_id='%s'"%(room_id)
            models.cursor.execute(getRoomQuery)
            roomData=models.cursor.fetchall()[0]
            print("userData :",userData,"roomData : ",roomData)
            if self.token:
                response=render(request, "user/bookRoom.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"userData":userData,"roomData":roomData})
            else:
                if 'token' in request.COOKIES:
                    self.token = request.COOKIES["token"]
                    response=render(request, "user/bookRoom.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"userData":userData,"roomData":roomData})
                else:
                    response= redirect(curl+"login/")
            return response
        else:
            order_id = "order"+getTimeStamp()
            room_id = request.POST.get('room_id')
            user_id = request.POST.get('user_id')
            joining_date = request.POST.get('joining_date')            
            booking_date = datetime.today().strftime('%d-%m-%Y')
            leaving_date = "NY"
            trxn_id = "dfnjskffdjmfdgjfd"
            bookRoomQuery = "insert into history (order_id,room_id,user_id,joining_date,booking_date,leaving_date,trxn_id) values('%s','%s','%s','%s','%s','%s','%s')"%(order_id,room_id,user_id,joining_date,booking_date,leaving_date,trxn_id)
            models.cursor.execute(bookRoomQuery)
            models.db.commit()
            return JsonResponse({"message":"Room book SuccessFully....!","curl":curl})
    def logout(self,request):
        if 'token' in request.COOKIES:
            response = redirect(curl)
            response.delete_cookie('token')
            self.token = None
        else:
            response = redirect(curl)
        return response