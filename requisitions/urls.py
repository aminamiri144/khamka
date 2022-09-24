from django.urls import path
from requisitions.views import RequestListView, RequestCreateView, RequestDetailView, RequestUpdateView


urlpatterns = [
    path('', RequestListView.as_view(), name='request-list'),
    path('create/<int:customer>', RequestCreateView.as_view(), name='request-create'),
    path('update/<str:pk>/', RequestUpdateView.as_view(), name='request-update'),
    path('detail/<str:pk>/', RequestDetailView.as_view(), name='request-detail'),
]


