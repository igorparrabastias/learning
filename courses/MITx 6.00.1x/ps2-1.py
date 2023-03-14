remaining_balance = balance

for _ in range(12):
    p = remaining_balance * monthlyPaymentRate
    ub = remaining_balance - p
    remaining_balance = ub + (annualInterestRate / 12) * ub
    # print("Partial balance: ", remaining_balance)

remaining_balance = round(remaining_balance, 2)
print("Remaining balance: ", remaining_balance)
