import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alemeno.settings')

# Configure Django settings
django.setup()

from CAS_Backend.models import Customer

df = pd.read_excel('customer_data.xlsx')

for index, row in df.iterrows():
    customer = Customer(
        first_name=row['First Name'],
        last_name=row['Last Name'],
        age=row['Age'],
        monthly_salary=row['Monthly Salary'],
        phone_number=row['Phone Number'],
        approved_limit=row['Approved Limit'],
    )
    customer.save()