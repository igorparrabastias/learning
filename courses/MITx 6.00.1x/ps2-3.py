# balance = 320000
# annualInterestRate = 0.2
# Lowest Payment:  29157.09

balance = 999999
annualInterestRate = 0.18
# Lowest Payment:  90325.02

n = 0
remaining_balance = balance

c1 = balance/12
c2 = (balance*(1+annualInterestRate)**12)/12
g = (c1 + c2) / 2
lowest_payment = c1

# Algol: bisection search
while abs(remaining_balance) > 0.1:
    c1 = round(c1, 2)
    c2 = round(c2, 2)
    g = round(g, 2)

    remaining_balance = balance
    lowest_payment = g
    lowest_payment += .01
    for _ in range(12):
        ub = remaining_balance - lowest_payment
        remaining_balance = ub + (annualInterestRate / 12) * ub

    if remaining_balance > 0:
        c1 = g
    else:
        c1 = balance/12
        c2 = g

    g = (c1 + c2) / 2

    n += 1

print("Lowest Payment: ", round(lowest_payment, 2))
