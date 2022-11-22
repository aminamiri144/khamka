from django.urls import path
from letters.views import LetterCreateView


urlpatterns = [
        path('create/<int:requestid>', LetterCreateView.as_view(), name='letter-create'),
]
