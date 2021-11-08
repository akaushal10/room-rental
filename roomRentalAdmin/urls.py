from django.urls import path
from django.contrib import admin
from . import views
urlpatterns=[
    path('',views.adminHome),
    path('addFlat/',views.flat),
    path('addRoom/',views.room),
    path('manageFlat/',views.flat),
    path('manageRoom/',views.room),
]