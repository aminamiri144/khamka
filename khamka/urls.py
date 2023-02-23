"""khamka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from khamka.views import PanelView, SoonView, UserLoginView, UserLogoutView, register_customer_request, registerrequest
from khamka.settings import ADMIN_URL

urlpatterns = [
    # path('', Index.as_view(), name='index'),
    path(f'{ADMIN_URL}/', admin.site.urls),
    path('requestions/', include('requisitions.urls')),
    path('customers/', include('customers.urls')),
    path('letters/', include('letters.urls')),
    path('', PanelView.as_view(), name="panel"),
    path('coming-soon/', SoonView.as_view(), name="soon"),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', registerrequest),
    path("select2/", include("django_select2.urls")),
    path('reg-customer-request/', register_customer_request, name='reg-cureq'), # register both customer and request in one form

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)
