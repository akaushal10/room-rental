from django.shortcuts  import render,redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.http import Http404
from django.core.files.storage import FileSystemStorage
# Create your views here.
from roomRental import models
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
class RoomRentalAdmin:
    def __init__(self):
        self.adminToken = False
        self.admin={}
    def adminHome(self,request):
        if self.adminToken:
            return redirect(curl+'myadmin/')
        else:            
            if 'adminToken' in request.COOKIES:
                token = request.COOKIES["adminToken"]
                data = decodeJWTToken(token)
                query="select * from admins where admin_id='%s' and admin_password='%s' "%(data["email"],data["password"])
                models.cursor.execute(query)
                admin=models.cursor.fetchall()
                if len(admin)>0:
                    self.admin = admin[0]
                    response=render(request, "admin/adminHome.html",{'curl': curl, 'media_url': media_url})
                else:
                    response = redirect(curl)
                    response.delete_cookie('adminToken')
                return response
            else:
                response=redirect(curl)
                return response

    def flat(request):
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
                return JsonResponse({"output":1})
            except:
                return JsonResponse({"output":0})
    def room(request):
        flat_query = "select * from flat_types"
        models.cursor.execute(flat_query)
        flatList = models.cursor.fetchall()
        if request.method=='GET':
            return render(request,"admin/addRoom.html",{'curl':curl,'flatList':flatList})
        elif request.method=='POST':
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
            return JsonResponse({"output":1})
        elif request.method=='DELETE':
            return JsonResponse({"output":0})
        else:
            return JsonResponse({"output":0})
    def logout(self,request):
        if 'adminToken' in request.COOKIES:
            response = redirect(curl)
            response.delete_cookie('adminToken')
            self.adminToken = None
        else:
            response = redirect(curl)
        return response