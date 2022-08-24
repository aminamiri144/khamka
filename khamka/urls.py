"""khamka URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static





def index(request):
    context = {}
    return render(request, 'panel.html', context=context)

def login(request):
    context = {}
    return render(request, 'login.html', context=context)

def registerrequest(request):
    context = {}
    return render(request, 'rere.html', context=context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('requestions/', include('requisitions.urls')),
    path('customers/', include('customers.urls')),
    path('letter/', include('letters.urls')),
    path('panel/', index),
    path('login/', login),
    path('register/', registerrequest),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)