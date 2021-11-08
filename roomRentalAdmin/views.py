from django.shortcuts  import render,redirect
from django.conf import settings
curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL 
from django.http.response import JsonResponse
from django.http import Http404
from django.core.files.storage import FileSystemStorage
# Create your views here.
from roomRental import models
import time

def getTimeStamp():
    [t1,t2] = str(time.time()).split(".")
    return t1+t2
def adminHome(request):
    response=render(request, "admin/adminHome.html",{'curl': curl, 'media_url': media_url})
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