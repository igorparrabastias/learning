# **Bubble Sort**

**Bubble sort** algorithm is an algorithm that sorts the array by comparing two adjacent elements and swaps them if they are not in the intended order. Here order can be anything like increasing order or decreasing order.
---
- The **bubble sort** is a simple algorithm that sorts a list of items in memory. Given an array, the code repeatedly compares each pair of adjacent items and swaps them if they are not in order. The process repeats until no more swaps occur. If it were possible to view the array while the sort is in progress, the low values would "bubble" to the top while the large values would sink to the bottom. 
 - The **bubble sort** is the least complex but also one of the slowest. Consider these sorts for simple arrays with less than a few hundred items.

## Advantages and disvantages
- This algorithm has several advantages. It is simple to write, easy to understand and it only takes a few lines of code. The data is sorted in place so there is little memory overhead and, once sorted, the data is in memory, ready for processing.
- The major disadvantage is the amount of time it takes to sort. The average time increases almost exponentially as the number of table elements increase. Ten times the number of items takes almost one hundred times as long to sort.

## Complexity
- Worst Case and Average case time complexity: If the array is in reverse order then this condition is the worst case and Its time complexity is O(n2)
- Best case time complexity: If the array is already sorted then it is the best-case scenario and its time complexity is O(n)
- Auxiliary Space: O(1). We have constant variables, swapped, temp and i. However, you might argue that you can’t sort the array, if you don’t have it in memory. In that case, the worst case space complexity would be O(n).

refs:  
https://www.geeksforgeeks.org/bubble-sort-algorithms-by-using-javascript/
https://www.techwalla.com/articles/advantages-disadvantages-of-bubble-sort