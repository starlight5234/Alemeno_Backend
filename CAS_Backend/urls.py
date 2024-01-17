from django.urls import path
from .views import api_home, RegisterCustomer, CheckEligibility, CreateLoan, ViewLoan, ViewLoanCust

urlpatterns = [
    path('', api_home, name='api-home'),
    path('register/', RegisterCustomer.as_view(), name='RegisterCustomer'),
    path('check-eligibility/', CheckEligibility.as_view(), name='check_eligibility'),
    path('create-loan/', CreateLoan.as_view(), name='create_loan'),
]
