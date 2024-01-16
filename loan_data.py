import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alemeno.settings')

# Configure Django settings
django.setup()

from CAS_Backend.models import Customer , Loan

df = pd.read_excel('loan_data.xlsx')

for index, row in df.iterrows():
    customer_id = row['Customer ID']
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        print(f"Customer with ID {customer_id} not found. Skipping.")
        continue

    loan = Loan(
        loan_id = row['Loan ID'],
        customer = customer,
        loan_amount = row['Loan Amount'],
        interest_rate = row['Interest Rate'],
        tenure = row['Tenure'],
        emis_paid_on_time = row['EMIs paid on Time'],
        start_date = row['Date of Approval'],
        end_date = row['End Date'],
        monthly_installment = row['Monthly payment'],
        repayments_left = max((int(row['Tenure']) - int(row['EMIs paid on Time'])), 0)
    )
    loan.save()