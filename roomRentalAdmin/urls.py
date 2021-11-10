from django.urls import path
from django.contrib import admin
from . import views
adminObj = views.RoomRentalAdmin()
urlpatterns=[
    path('',adminObj.adminHome),
    path('addFlat/',adminObj.flat),
    path('addRoom/',adminObj.room),
    path('manageFlat/',adminObj.flat),
    path('manageRoom/',adminObj.room),
    path('logout/',adminObj.logout),
]