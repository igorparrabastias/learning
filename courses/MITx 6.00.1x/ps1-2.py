arr = list(s)
n = 0

while (len(arr) > 2):
    if (arr[0] + arr[1] + arr[2] == 'bob'):
        n += 1
    del arr[0]

print("Number of times bob occurs is: ", n)
