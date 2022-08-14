from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def request_detail(request, rid):
    return HttpResponse(f"test is {rid}")


def requests_archive(request, year=None, month=None, day=None):
    return HttpResponse(f'load the archive of {year}/{month}/{day}')