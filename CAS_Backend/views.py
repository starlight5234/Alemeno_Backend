from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import serialize
from django.http import JsonResponse

from .serializers import CustomerSerializer
from .models import Customer
from .helper import CheckLoanEligibility

# Create your views here.
def api_home(request):
    return JsonResponse({'message': 'Welcome to the API!'})

class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data

            # Calculate approved limit based on salary
            monthly_salary = data['monthly_salary']
            approved_limit = round(36 * monthly_salary / 100000) * 100000

            # Create a new customer
            customer = Customer.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                monthly_salary=monthly_salary,
                phone_number=data.get('phone_number', ''),
                approved_limit=approved_limit,
            )

            response_data = {
                'customer_id': customer.customer_id,
                'name': f"{customer.first_name} {customer.last_name}",
                'age': customer.age,
                'monthly_income': customer.monthly_salary,
                'approved_limit': customer.approved_limit,
                'phone_number': customer.phone_number
            }
        
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckEligibility(APIView):
    def post(self, request):
        data = request.data
        customer_id  = data['customer_id']

        if Customer.objects.filter(pk=customer_id).exists():
            customer = Customer.objects.get(pk=customer_id)
            interest_rate  = data['interest_rate']
            loan_amount  = data['loan_amount']
            tenure  = data['tenure']
            approval, interest = CheckLoanEligibility(customer_id, interest_rate)

            response_data = {
                "customer_id": customer_id,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "approval": approval,
                "corrected_interest_rate": interest,
                "tenure": tenure
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
        else:
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
