"""
Created on Wed Jun  8 12:09:59 2016

@author: ericgrimson
"""


num = 11

if num < 0:
    isNeg = True
    num = abs(num)
else:
    isNeg = False

result = '0' if num == 0 else ''
while num > 0:
    result = str(num % 2) + result
    print('result:', result)
    num = num//2
    print('num:', num)
if isNeg:
    result = '-' + result

print(result)
