
from django.urls import path, include
from django.shortcuts import render
from customers.views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDetailView


urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-list'),
    path('create/', CustomerCreateView.as_view(), name='customer-create'),
    path('update/<str:pk>/', CustomerUpdateView.as_view(), name='customer-update'),
    path('detail/<str:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
]