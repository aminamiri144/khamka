from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from requisitions.models import Request
from requisitions.serializers import RequestSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]