
from django.urls import path, include
from django.shortcuts import render





def index(request):
    context = {}
    return render(request, 'customers/datalist.html', context=context)


urlpatterns = [
    path('list/', index),
]