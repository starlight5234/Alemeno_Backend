from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import serialize
from django.http import JsonResponse

from .serializers import CustomerSerializer, LoanSerializerView
from .models import Customer, Loan
from .helper import CalculateMonthlyInstallment, CheckLoanEligibility

from datetime import date, timedelta

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

class CreateLoan(APIView):
    def post(self, request):
        data = request.data
        customer_id  = data['customer_id']
        interest_rate  = data['interest_rate']
        loan_amount  = data['loan_amount']
        tenure  = data['tenure']
        message = "Approved"


        if Customer.objects.filter(pk=customer_id).exists():
            customer = Customer.objects.get(pk=customer_id)
            approval, corrected_interest = CheckLoanEligibility(customer_id, interest_rate)
            monthly_installment = 0

            response_data = {
                "customer_id": customer_id,
                "loan_amount": loan_amount,
                "interest_rate": corrected_interest,
                "approval": approval,
                "message": message,
            }
            
            if approval == True:
                monthly_installment = CalculateMonthlyInstallment(loan_amount, interest_rate,tenure)

                response_data["monthly_installment"] = monthly_installment

                new_loan = Loan.objects.create(
                    customer = customer,
                    loan_amount=loan_amount,
                    interest_rate = corrected_interest,
                    tenure = tenure,
                    monthly_installment = monthly_installment,
                    start_date = date.today(),
                    end_date = date.today() + timedelta(days = 30 * tenure),
                    repayments_left = tenure
                )

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data["message"] = "Disapproved"
                return Response(response_data,status=status.HTTP_200_OK)
        else:
            return Response({"message": "Customer not found"},status=status.HTTP_404_NOT_FOUND)

class ViewLoan(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LoanSerializerView(loan)
        serializer.data['customer'].pop('monthly_salary')
        return Response(serializer.data, status=status.HTTP_200_OK)

class ViewLoanCust(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id = customer_id)
            loans = Loan.objects.filter(customer = customer)

            response = []

            for loan in loans:
                entry = LoanSerializerView(loan).data
                entry["customer"].pop('monthly_salary')
                response.append(entry)

            return Response(response, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
