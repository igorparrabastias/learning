# Merge Sort

The **Merge Sort** algorithm is a sorting algorithm that is based on the Divide and Conquer paradigm. In this algorithm, the array is initially divided into two equal halves and then they are combined in a sorted manner.

The merge algorithm consists of two functions:
- The mergeSort function, which takes care of partitioning the arrays.
- The merge function, which merges the separate arrays.

## Complexity
- The **merge sort** algorithm has the time complexity of O(logN), meaning that the time required to execute N number of elements will rise in logarithmic proportion. If sorting an array of 10 elements requires 1ms, sorting an array of 100 elements will take 2ms.
- **Merge sort** is much more efficient in time complexity than the **insertion sort**, but **merge sort** also consumes more space because the sorting is not in-place and the recursive call will be threaded. The **merge sort** will take O(N) space to perform the sorting.

## Complexity 2
- The worst-case time complexity of **Merge Sort** is O(nlogn), same as that for best case time complexity for **Quick Sort**. When it comes to speed, **Merge Sort** is one of the fastest sorting algorithms out there.
- Unlike **Quick Sort**, **Merge Sort** is not an in-place sorting algorithm, meaning it takes extra space other than the input array. This is because we are using auxiliary (helper) arrays to store the sub-arrays. The space complexity of the **merge sort** is O(n).
- Another advantage of **Merge Sort** is that it lends itself very well to multi-threading, since each respective half and be sorted on its own. Another common way of reducing the runtime of **Merge Sort** is to stop when we get to relatively small subarrays (~7) and using **Insertion Sort** to sort them.
- This is done because **Insertion Sort** performs really well on small, or nearly sorted arrays. Much better than it's more globally efficient counterparts.

## Drawbacks of Merge Sort:
- Slower compared to the other sort algorithms for smaller tasks.
- The **merge sort** algorithm requires an additional memory space of 0(n) for the temporary array.
- It goes through the whole process even if the array is sorted.

refs: 
- https://www.geeksforgeeks.org/merge-sort/
- https://stackabuse.com/merge-sort-in-javascript/
- https://sebhastian.com/merge-sort-javascript

