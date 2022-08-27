from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from requisitions.models import Request
from requisitions.serializers import RequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        custom_data = {
            'data': RequestSerializer(self.get_queryset(),many=True).data,
        }
        return Response(custom_data)
