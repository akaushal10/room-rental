from django.shortcuts import render,redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.core.files.storage import FileSystemStorage
from roomRental import models
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from . import paytm_checksum as paytm
import time
import jwt

curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL 
jwt_key = settings.JWT_SECURITY_KEY
jwt_algo = 'HS256'
MERCHANT_KEY=settings.MERCHANT_KEY
MID=settings.MID
def getTimeStamp():
    [t1,t2] = str(time.time()).split(".")
    return t1+t2

def createJWTToken(data):
    return jwt.encode(data,jwt_key,jwt_algo)
def decodeJWTToken(data):
    return jwt.decode(data, jwt_key, algorithms=[jwt_algo])
from datetime import datetime, timedelta


def inc_date(origin_date):
    day = origin_date.day
    month = origin_date.month
    year = origin_date.year
    if origin_date.month == 12:
        delta = datetime(year + 1, 1, day) - origin_date
    else:
        delta = datetime(year, month + 1, day) - origin_date
    return origin_date + delta

class User:
    def __init__(self):
        self.token = False
        self.user = []
    def userHome(self,request):
        roomQuery = "select * from room_types limit 3"
        models.cursor.execute(roomQuery)
        roomsList = models.cursor.fetchall()
        if self.token:
            response=render(request, "user/userHome.html",{'curl': curl, 'media_url': media_url,"user":self.user,"isLogin":True,'rooms':roomsList})
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
                    response=render(request, "user/userHome.html",{'curl': curl, 'media_url': media_url,"user":self.user,"isLogin":True,'rooms':roomsList})
                else:
                    response= redirect(curl)
                return response
            else:
                response= redirect(curl)
                return response
    def about(self,request):
        if self.token:
            response=render(request, "about.html",{'curl': curl, 'media_url': media_url,"isLogin":True})
        else:
            if 'token' in request.COOKIES:
                response=render(request, "about.html",{'curl': curl, 'media_url': media_url,"isLogin":True})
            else:
                response=redirect(curl+"about/")
        return response
    def help(self,request):
        getHelpQuery = "select * from helps"
        models.cursor.execute(getHelpQuery)
        helps = models.cursor.fetchall()
        if self.token:
            response=render(request, "help.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"helps":helps})
        else:
            if 'token' in request.COOKIES:
                response=render(request, "help.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"helps":helps})
            else:
                response=redirect(curl+"help/")
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
        getFlatName = "select flat_name from flat_types where flat_id = '%s'"%(flatId)
        models.cursor.execute(getFlatName)
        flatName = models.cursor.fetchall()[0][0]

        getRoomsQuery = "select * from room_types where flat_id='%s'"%(flatId)
        models.cursor.execute(getRoomsQuery)
        rooms = models.cursor.fetchall()
        if self.token:
            response=render(request, "rooms.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"rooms":rooms,"flatName":flatName})
        else:
            if 'token' in request.COOKIES:
                self.token = request.COOKIES["token"]
                response=render(request, "rooms.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"rooms":rooms,"flatName":flatName})
            else:
                response= redirect(curl+"flatType/")
        return response
    def history(self,request):
        data = decodeJWTToken(request.COOKIES["token"])
        getUserQuery="select user_id from user where email='%s' and password='%s' "%(data["email"],data["password"])
        models.cursor.execute(getUserQuery)
        userData=models.cursor.fetchall()[0]

        getHistoryQuery = "select history.joining_date,history.leaving_date,history.booking_date,room_types.room_add,room_types.room_price,room_types.room_img from history inner join room_types on room_types.room_id=history.room_id where history.user_id='%s'"%(userData[0]) 
        models.cursor.execute(getHistoryQuery)
        rooms = models.cursor.fetchall()
        if self.token:
            response=render(request, "user/userHistory.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"history":rooms})
        else:
            if 'token' in request.COOKIES:
                self.token = request.COOKIES["token"]
                response=render(request, "user/userHistory.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"history":rooms})
            else:
                response= redirect(curl+"flatType/")
        return response

    def bookRoom(self,request):
        if 'token' in request.COOKIES:
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
                self.order_id = "order"+getTimeStamp()
                self.room_id = request.POST.get('room_id')
                self.user_id = request.POST.get('user_id')
                self.price = request.POST.get('price')
                joining_date = request.POST.get('joining_date')       
                total_months = int(request.POST.get('total_months'))
                temp_date = datetime.strptime(joining_date, "%Y-%m-%d")
                self.joining_date = temp_date.strftime('%d-%m-%Y')
                leaving_date = temp_date
                for i in range(total_months):
                    leaving_date = inc_date(leaving_date)
                self.leaving_date = leaving_date.strftime('%d-%m-%Y')
                self.booking_date = datetime.today().strftime('%d-%m-%Y')
                
                self.param_dict={
                    'MID':MID,
                    'ORDER_ID':self.order_id,
                    'TXN_AMOUNT':str(self.price*total_months),
                    'CUST_ID':self.user_id,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE':'WEBSTAGING',
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':curl+'myuser/checkout/',
                }
                self.param_dict['CHECKSUMHASH']=paytm.generate_checksum(self.param_dict,MERCHANT_KEY)
                return JsonResponse({"message":"Room book SuccessFully....!","curl":curl})            
        else:
            return redirect(curl+"login/")
    @csrf_exempt
    def checkout(self,request):
        if request.method=="GET":
            return render(request,"paytm.html",{"param_dict":self.param_dict})
        else:
            form=request.POST
            response_dict=dict()
            for i in form.keys():
                response_dict[i]=form[i]
                if i == 'CHECKSUMHASH' :
                    checksum=form[i]
            print(response_dict)
            verify=paytm.verify_checksum(response_dict,MERCHANT_KEY,checksum)
            if(verify):
                bookRoomQuery = "insert into history (order_id,room_id,user_id,joining_date,booking_date,leaving_date,trxn_id) values('%s','%s','%s','%s','%s','%s','%s')"%(self.order_id,self.room_id,self.user_id,self.joining_date,self.booking_date,self.leaving_date,response_dict['TXNID'])
                models.cursor.execute(bookRoomQuery)
                models.db.commit()

                trxnQuery = "insert into transactions (BANKNAME,BANKTXNID,CURRENCY,PAYMENTMODE,MID,TXNID,TXNAMOUNT,ORDERID,TXNDATE) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(response_dict['BANKNAME'],response_dict['BANKTXNID'],response_dict['CURRENCY'],response_dict['PAYMENTMODE'],response_dict['MID'],response_dict['TXNID'],response_dict['TXNAMOUNT'],response_dict['ORDERID'],response_dict['TXNDATE'])
                models.cursor.execute(trxnQuery)
                models.db.commit()
                return redirect(curl+'myuser/history')
            else:
                return redirect(curl+'myuser')

    def logout(self,request):
        if 'token' in request.COOKIES:
            response = redirect(curl)
            response.delete_cookie('token')
            self.token = None
        else:
            response = redirect(curl)
        return response