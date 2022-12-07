from django.urls import path
from letters.views import LetterCreateView, OrganCreateView


urlpatterns = [
        path('create/<int:requestid>', LetterCreateView.as_view(), name='letter-create'),
        path('organ/create/<int:craete_letter_id>', OrganCreateView.as_view(), name='organ-create'),
]
