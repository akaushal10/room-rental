from django.shortcuts import render
from django.conf import settings
curl=settings.CURRENT_URL
media_url=settings.MEDIA_URL 
from django.http.response import JsonResponse
from django.core.files.storage import FileSystemStorage
from roomRental import models
import time

def userHome(request):
    print("USer HJOme")
    response=render(request, "home.html",{'curl': curl, 'media_url': media_url})
    return response