from django.urls import path
from requisitions.views import RequestListView, RequestCreateView, RequestDetailView, RequestUpdateView, AttachmentCreateView, AttachmentDeleteView


urlpatterns = [
    path('', RequestListView.as_view(), name='request-list'),
    path('create/<int:customer>', RequestCreateView.as_view(), name='request-create'),
    path('update/<str:pk>/', RequestUpdateView.as_view(), name='request-update'),
    path('detail/<str:pk>/', RequestDetailView.as_view(), name='request-detail'),
    path('create/attachment/<str:pk>/', AttachmentCreateView.as_view(), name='attachment-create'),
    path('delete/attachment/<pk>/', AttachmentDeleteView.as_view(), name='attachment-delete'),
]


