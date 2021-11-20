from django.urls import path
from django.contrib import admin
from . import views
adminObj = views.RoomRentalAdmin()
urlpatterns=[
    path('',adminObj.adminHome),
    path('addFlat/',adminObj.flat),
    path('addRoom/',adminObj.room),
    path('help/',adminObj.help),
    path('getOrderHistory/',adminObj.getOrderHistory),
    path('manageFlat/',adminObj.flat),
    path('manageRoom/',adminObj.manageRoom),
    path('trxn/',adminObj.trxn),
    path('logout/',adminObj.logout),
]