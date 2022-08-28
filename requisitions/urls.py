
from rest_framework.routers import DefaultRouter
from requisitions.views import RequestViewSet
from django.shortcuts import render
from django.urls import path


router = DefaultRouter()
router.register(r'request', RequestViewSet, basename='request') 

def index(request):
    context = {}
    return render(request, 'requests/datalist.html', context=context)

urlpatterns = [
        path('list/', index),
] 

urlpatterns += router.urls
