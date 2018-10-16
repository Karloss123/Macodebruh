#paying debt off dat credit-card bruh. mad money bruh.

def cred_card_balance(balance, annualInterestRate,monthlyPaymentRate):  
    monthly_interest_rate = annualInterestRate/12.0
    count = 1
    while count <= 12:
        min_monthly_payment = monthlyPaymentRate * balance
        monthly_unpaid_bal = balance - min_monthly_payment
        updated_balance = monthly_unpaid_bal + monthly_interest_rate * monthly_unpaid_bal
        balance = updated_balance
        count += 1
    rounded_balance = round(balance,2)
    print("Remaining Balance: " + str(rounded_balance))
    
