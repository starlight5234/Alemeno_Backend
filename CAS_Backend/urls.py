from django.urls import path
from .views import api_home, RegisterCustomer

urlpatterns = [
    path('', api_home, name='api-home'),
    path('register/', RegisterCustomer.as_view(), name='RegisterCustomer'),
]
