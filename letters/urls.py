from django.urls import path
from letters.views import LetterCreateView, OrganCreateView, LetterListView, LetterDetailView, LetterUpdateView


urlpatterns = [
        path('', LetterListView.as_view(), name='letter-list'),
        # path('rcreate/<int:requestid>', LetterRCreateView.as_view(), name='letter-rcreate'),
        path('update/<int:pk>', LetterUpdateView.as_view(), name='letter-update'),
        path('create/', LetterCreateView.as_view(), name='letter-create'),
        path('detail/<int:pk>', LetterDetailView.as_view(), name='letter-detail'),
        path('organ/create', OrganCreateView.as_view(), name='organ-create'),
]
