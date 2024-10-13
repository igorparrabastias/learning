vowels = ['a', 'e', 'i', 'o', 'u']
n = 0
for i in list(s):
    if i in vowels:
        n = n + 1
print("Number of vowels: ", n)
