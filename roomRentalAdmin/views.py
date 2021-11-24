from django.shortcuts  import render,redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.http import Http404
from django.core.files.storage import FileSystemStorage
# Create your views here.
from roomRental import models
import time
import jwt
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict


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
class RoomRentalAdmin:
    def __init__(self):
        self.adminToken = False
        self.admin={}
    def adminHome(self,request):
        getHistory = "select * from history"
        models.cursor.execute(getHistory)
        rooms = models.cursor.fetchall()
        if self.adminToken:
            print("self.tokken")
            response=render(request, "admin/adminHome.html",{'curl': curl, 'media_url': media_url,"history":rooms})
        else:            
            if 'adminToken' in request.COOKIES:
                token = request.COOKIES["adminToken"]
                data = decodeJWTToken(token)
                query="select * from admins where admin_id='%s' and admin_password='%s' "%(data["email"],data["password"])
                models.cursor.execute(query)
                admin=models.cursor.fetchall()
                if len(admin)>0:
                    self.admin = admin[0]
                    print("if conditi")
                    response=render(request, "admin/adminHome.html",{'curl': curl, 'media_url': media_url,"history":rooms})
                else:
                    response = redirect(curl)
                    response.delete_cookie('adminToken')
                return response
            else:
                response=redirect(curl)
        return response
    def getOrderHistory(self,request):
        orderId = request.POST.get('orderId')
        getOrderInfoQuery = "SELECT order_id,joining_date,booking_date,leaving_date,trxn_id,name,mobile,room_add,TXNAMOUNT from history inner join user on history.user_id=user.user_id INNER join room_types on history.room_id=room_types.room_id INNER JOIN transactions ON history.trxn_id=transactions.TXNID WHERE history.order_id='%s'"%(orderId)
        models.cursor.execute(getOrderInfoQuery)
        orderInfo = models.cursor.fetchall()[0]
        print(orderInfo)
        return JsonResponse({"data":{"address":orderInfo[7],"name":orderInfo[5],"contact":orderInfo[6],"bookedOn":orderInfo[2],"joinedOn":orderInfo[1],"leaveOn":orderInfo[3],"trxnId":orderInfo[4],"trxnAmount":orderInfo[8],"bookingId":orderInfo[0]}})

    def flat(self,request):
        if request.method=='GET':
            response=render(request, "admin/addFlat.html",{'curl': curl, 'media_url': media_url})
            return response
        else:
            try:
                flat_name = request.POST.get('flat_name')
                flat_id = "flat"+getTimeStamp()
                query = "insert into flat_types values(%s,%s)"
                val= (flat_id,flat_name)
                models.cursor.execute(query,val)
                models.db.commit()
                return JsonResponse({"message":"Falt added succesfully...!"})
            except:
                return JsonResponse({"error":"Something went wrong...!"})

    @csrf_exempt
    def help(self,request):
        getHelpQuery = "select * from helps"
        models.cursor.execute(getHelpQuery)
        helps = models.cursor.fetchall()
        print(request.method)
        if request.method=='GET':
            response=render(request, "admin/addHelp.html",{'curl': curl, 'media_url': media_url,"helps":helps})
            return response
        elif request.method=='POST':
            try:
                question = request.POST.get('question')
                answer = request.POST.get('answer')
                helpId = "help"+getTimeStamp()
                insertHelp = "insert into helps values('%s','%s','%s')"%(helpId,question,answer)
                models.cursor.execute(insertHelp)
                models.db.commit()
                return JsonResponse({"message":"Help added succesfully...!","help":{"id":helpId,"question":question,"answer":answer}})
            except:
                return JsonResponse({"error":"Something went wrong...!"})
        else:
            return JsonResponse({"error":"Something went wrong...!"})

    def deleteHelp(self,request):
        helpId = request.POST.get('helpId')
        print("helpId : ",helpId)
        deleteHelp = "delete from helps where help_id='%s'"%(helpId)
        models.cursor.execute(deleteHelp)
        models.db.commit()
        return JsonResponse({"message":"Help deleted...!"})

    def room(self,request):
        flat_query = "select * from flat_types"
        models.cursor.execute(flat_query)
        flatList = models.cursor.fetchall()
        if request.method=='GET':
            return render(request,"admin/addRoom.html",{'curl':curl,'flatList':flatList})
        elif request.method=='POST':
            try:
                flat_id=request.POST.get('flat_id')
                room_desc=request.POST.get('room_desc')
                room_add=request.POST.get('room_add')
                room_price=request.POST.get('room_price')
                room_img=request.FILES['room_img']
                room_id = "room"+getTimeStamp()
                fs=FileSystemStorage()
                filename=fs.save(room_img.name,room_img)
                query = "insert into room_types (flat_id,room_id,room_desc,room_img,room_price,room_add) values('%s','%s','%s','%s',%d,'%s')"%(flat_id,room_id,room_desc,filename,int(room_price),room_add)
                models.cursor.execute(query)
                models.db.commit()
                return JsonResponse({"message":"Room added succesfully...!"})
            except:
                return JsonResponse({"error":"Something went wrong...!"})
        elif request.method=='DELETE':
            return JsonResponse({"output":0})
        else:
            return JsonResponse({"output":0})

    @csrf_exempt
    def manageRoom(self,request):
        getRoomsQuery =  "select * from room_types inner join flat_types on flat_types.flat_id=room_types.flat_id;"
        models.cursor.execute(getRoomsQuery)
        roomData = models.cursor.fetchall()

        flat_query = "select * from flat_types"
        models.cursor.execute(flat_query)
        flatList = models.cursor.fetchall()

        if request.method=='GET':
            return render(request,"admin/manageRoom.html",{'curl':curl,'rooms':roomData,'flatList':flatList})
        elif request.method=='POST':
            flat_id=request.POST.get('flat_id')
            room_id=request.POST.get('room_id')
            room_desc=request.POST.get('room_desc')
            room_add=request.POST.get('room_add')
            room_price=request.POST.get('room_price')
            updateRoomQuery = "update room_types set room_desc='%s',room_add='%s',room_price='%s',flat_id='%s' where room_id='%s' "%(room_desc,room_add,int(room_price),flat_id,room_id)
            models.cursor.execute(updateRoomQuery)
            models.db.commit()
            return JsonResponse({"message":"Room updated succesfully...!"})
            # except:
            #     return JsonResponse({"error":"Something went wrong...!"})    
        else:
            return JsonResponse({"error":"Something went wrong...!"})    

    def trxn(self,request):
        getTransactions = "select * from transactions"
        models.cursor.execute(getTransactions)
        trxns = models.cursor.fetchall()
        if self.adminToken:
            response=render(request, "admin/trxn.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"trxns":trxns})
        else:
            if 'adminToken' in request.COOKIES:
                self.adminToken = request.COOKIES["adminToken"]
                response=render(request, "admin/trxn.html",{'curl': curl, 'media_url': media_url,"isLogin":True,"trxns":trxns})
            else:
                response= redirect(curl)
        return response
    def logout(self,request):
        if 'adminToken' in request.COOKIES:
            response = redirect(curl)
            response.delete_cookie('adminToken')
            self.adminToken = None
        else:
            response = redirect(curl)
        return response