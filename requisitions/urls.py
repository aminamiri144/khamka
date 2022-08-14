from urllib import request
from django.urls import path
from requisitions.views import request_detail, requests_archive


urlpatterns = [
    path('detail/<str:rid>/', request_detail),
    path('archive/<int:year>/<int:month>/<int:day>/', requests_archive)
]
