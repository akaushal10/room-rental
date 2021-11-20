from django.urls import path
from django.contrib import admin
from . import views
user = views.User()
urlpatterns=[
    path('',user.userHome),
    path('flatType/',user.flatType),
    path('rooms/',user.rooms),
    path('about/',user.about),
    path('help/',user.help),
    path('bookRoom/',user.bookRoom),
    path('history/',user.history),
    path('logout/',user.logout),
    path('checkout/',user.checkout)
]