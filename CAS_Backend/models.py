from django.db import models

from decimal import Decimal, ROUND_HALF_EVEN
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    phone_number = models.CharField(max_length=10)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(180)]) # Set to 180 for now acc to data given
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    repayments_left = models.PositiveIntegerField(default=0)
