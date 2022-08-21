from django.urls import path
from letters.views import LetterListAPI


urlpatterns = [
    path('list/', LetterListAPI.as_view(), name='letters-list'),
]
