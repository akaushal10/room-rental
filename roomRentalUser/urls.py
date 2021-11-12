from django.urls import path
from django.contrib import admin
from . import views
user = views.User()
urlpatterns=[
    path('',user.userHome),
    path('flatType/',user.flatType),
    path('rooms/',user.rooms),
    path('bookRoom/',user.bookRoom),
    path('history/',user.history),
    path('logout/',user.logout),
    path('checkout/',user.checkout)
]