from django.urls import path
from letters.views import LetterCreateView, OrganCreateView, LetterListView, LetterDetailView,LetterScreateView


urlpatterns = [
        path('', LetterListView.as_view(), name='letter-list'),
        path('create/<int:requestid>', LetterCreateView.as_view(), name='letter-create'),
        path('rcreate/', LetterScreateView.as_view(), name='letter-rcreate'),
        path('detail/<int:pk>', LetterDetailView.as_view(), name='letter-detail'),
        path('organ/create/<int:craete_letter_id>', OrganCreateView.as_view(), name='organ-create'),
]
