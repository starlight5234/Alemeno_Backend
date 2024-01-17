from datetime import datetime
from django.utils import timezone
from .models import Customer, Loan

def PastLoanPaidOnTime(customer_id):
    loans = Loan.objects.filter(customer_id=customer_id)
    loan_approved_volume = 0
    total_loan_taken = loans.count()
    loans_in_current_year = 0
    
    if not loans.exists():
       return 100, loan_approved_volume, total_loan_taken, loans_in_current_year, 0
    
    # Find past loans completed with tenure
    current_year = datetime.now().year
    curr_date = timezone.now().date()
    loans_in_current_year = loans.filter(start_date__year=current_year).count()
    total_loans = 0
    paid_on_time = 0
    loan_approved_volume = 0
    sum_of_current_loan = 0

    for loan in loans:
        loan_approved_volume += loan.loan_amount
        if loan.end_date < curr_date:
            total_loans += 1
            if loan.emis_paid_on_time == loan.tenure:
                paid_on_time += 1
        else:
            sum_of_current_loan += loan.loan_amount
 
    #print(loan_approved_volume, total_loan_taken, loans_in_current_year, sum_of_current_loan)

    if total_loans == 0:
        return 100, loan_approved_volume, total_loan_taken, loans_in_current_year, sum_of_current_loan

    # Calculate the percentage of loans paid on time
    if total_loans > 0:
        percentage_paid_on_time = (paid_on_time/total_loans) * 100
    else:
        percentage_paid_on_time = 0
        
    return percentage_paid_on_time, loan_approved_volume, total_loan_taken, loans_in_current_year, sum_of_current_loan


def CheckLoanEligibility(customer_id, interest_rate):
    percentage_paid_on_time, loan_approved_volume, total_loan_taken, loans_in_current_year, sum_current_loan = PastLoanPaidOnTime(customer_id)
    
    # Set weights for each criterion (you can adjust these based on your business rules)
    weight_percentage_paid_on_time = 0.4
    weight_loan_approved_volume = 0.2
    weight_total_loan_taken = 0.2
    weight_loans_in_current_year = 0.2

    # Define the maximum expected values for normalization
    max_loan_approved_volume = 100000  # Dummy value
    max_total_loan_taken = 10  # Dummy value
    max_loans_in_current_year = 5  # Dummy value

    weighted_sum = (
        weight_percentage_paid_on_time * (percentage_paid_on_time / 100) +
        weight_loan_approved_volume * float((loan_approved_volume / max_loan_approved_volume)) +
        weight_total_loan_taken * (total_loan_taken / max_total_loan_taken) +
        weight_loans_in_current_year * (loans_in_current_year / max_loans_in_current_year)
    )

    # Map the weighted sum to the credit rating scale (0 to 100)
    credit_rating = int(weighted_sum * 100)

    # Ensure credit rating is within the valid range (0 to 100)
    credit_rating = max(0, min(100, credit_rating))
 
    # Retrieve customer data
    credit_rating = percentage_paid_on_time * .25 + total_loan_taken
    monthly_salary = Customer.objects.get(pk=customer_id).monthly_salary

    # Implement credit approval logic
    if credit_rating > 50:
        approval = True
        corrected_interest_rate = interest_rate
    elif 50 > credit_rating > 30:
        if interest_rate > 12:
            approval = True
            corrected_interest_rate = interest_rate
        else:
            approval = False
            corrected_interest_rate = 12
    elif 30 > credit_rating > 10:
        if interest_rate > 16:
            approval = True
            corrected_interest_rate = interest_rate
        else:
            approval = False
            corrected_interest_rate = 16
    else:
        approval = False
        corrected_interest_rate = 0
        print("Insufficient Credit score")

    if sum_current_loan > 0.5 * float(monthly_salary):
        approval = False
        corrected_interest_rate = 0
        print("EMI greater than salary")
    
    print(credit_rating)
    return approval, corrected_interest_rate
