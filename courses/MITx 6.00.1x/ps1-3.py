s = 'abcbcd'
arr = list(s)
longest_test = arr.pop(0)
longest_candidate = longest_test
previous = ord(longest_test)

for idx, val in enumerate(arr):
    ord_val = ord(val)
    if (ord_val >= previous):
        longest_test = longest_test + val

        if len(longest_test) > len(longest_candidate):
            longest_candidate = longest_test
    else:
        if len(longest_test) > len(longest_candidate):
            longest_candidate = longest_test
        # reset
        longest_test = val
    previous = ord_val

print("Longest substring in alphabetical order is: ", longest_candidate)
