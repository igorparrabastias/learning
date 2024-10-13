remaining_balance = balance
lowest_payment = -10

while remaining_balance > 0:
    remaining_balance = balance
    lowest_payment += 10
    for _ in range(12):
        ub = remaining_balance - lowest_payment
        remaining_balance = ub + (annualInterestRate / 12) * ub

print("Lowest Payment: ", round(lowest_payment, 2))
