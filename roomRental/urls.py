"""roomRental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from distutils.command.register import register
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
guest = views.Guest()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',guest.home),
    path('adminLogin/',guest.adminLogin),
    path('login/',guest.login),
    path('signup/',guest.signup),
    path('flatType/',guest.flatType),
    path('rooms/',guest.rooms),
    path('myadmin/',include('roomRentalAdmin.urls')),
    path('myuser/',include('roomRentalUser.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
