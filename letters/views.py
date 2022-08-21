from operator import le
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from letters.models import Letter
# Create your views here.


class LetterListAPI(APIView):

    def get(self, request, *args, **kwargs):
        letters = Letter.objects.all().values('letter_number', 'title')
        return Response(letters)
