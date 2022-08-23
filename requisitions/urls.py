from urllib import request
from django.urls import path
from rest_framework.routers import DefaultRouter
from requisitions.views import RequestViewSet


router = DefaultRouter()
router.register(r'request', RequestViewSet, basename='request') 


urlpatterns = [

] 

urlpatterns += router.urls
