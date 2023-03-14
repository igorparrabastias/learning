# QuickSort

Like **Merge Sort**, **QuickSort** is a Divide and Conquer algorithm. As **quicksort** doesn’t use any space, it’s a in-place sorting algorithm. The way **quicksort** works is by choosing a pivot (an element in the array, often random, first, last, median), and check whether values in the array are higher or lower than that pivot. The values lower than the pivot should be on the left side, and the values higher than the pivot should be on the right side!

- Over the years, many sorting algorithms have been developed, and one of the **fastest** ones to date is **Quicksort**.
- **Quicksort** uses the divide-and-conquer strategy to sort the given list of elements. This means that the algorithm breaks down the problem into subproblems until they become simple enough to solve directly.
- Algorithmically this can be implemented either recursively or iteratively. However, the recursive approach is more natural for this problem.

## Default sorting in JavaScript (What is the reason to choose Quick sort over default sort() in JavaScript)
- JavaScript has sort(). Let us take an example with few array of elements like [5,3,7,6,2,9] and want to sort this array elements in ascending order. Just call sort() on items array and it sorts array elements in ascending order.
- Though sort() gives the result we want, problem lies with the way it sorts the array elements. Default sort() in JavaScript uses **Insertion sort** by V8 Engine of Chrome and **Merge sort** by Mozilla Firefox and Safari.
- But, other this is not suitable if you need to sort large number of elements. So, the solution is to use **Quick sort** for large dataset.

## Complexity
- Best and average: Each partitioning takes O(n) operations, and every partitioning splits the array O(log(n)). This results in O(n log(n)).
- Worst: If you always pick a pivot that is the highest or lowest value, you need to iterate through the entire array. O(n2)
- Worst space: The number of variables that are stored


## Why Quick Sort is preferred over MergeSort for sorting Arrays ?
**Quick Sort** in its general form is an in-place sort (i.e. it doesn’t require any extra storage) whereas **merge sort** requires O(N) extra storage, N denoting the array size which may be quite expensive. Allocating and de-allocating the extra space used for **merge sort** increases the running time of the algorithm. Comparing average complexity we find that both type of sorts have O(NlogN) average complexity but the constants differ. For arrays, **merge sort** loses due to the use of extra O(N) storage space.
Most practical implementations of **Quick Sort** use randomized version. The randomized version has expected time complexity of O(nLogn). The worst case is possible in randomized version also, but worst case doesn’t occur for a particular pattern (like sorted array) and randomized **Quick Sort** works well in practice.
**Quick Sort** is also a cache friendly sorting algorithm as it has good locality of reference when used for arrays.
**Quick Sort** is also tail recursive, therefore tail call optimizations is done.

## Why MergeSort is preferred over QuickSort for Linked Lists ? 
In case of linked lists the case is different mainly due to difference in memory allocation of arrays and linked lists. Unlike arrays, linked list nodes may not be adjacent in memory. Unlike array, in linked list, we can insert items in the middle in O(1) extra space and O(1) time. Therefore merge operation of **merge sort** can be implemented without extra space for linked lists.
In arrays, we can do random access as elements are continuous in memory. Let us say we have an integer (4-byte) array A and let the address of A[0] be x then to access A[i], we can directly access the memory at (x + i*4). Unlike arrays, we can not do random access in linked list. **Quick Sort** requires a lot of this kind of access. In linked list to access i’th index, we have to trprevavel each and every node from the head to i’th node as we don’t have continuous block of memory. Therefore, the overhead increases for **quick sort**. **Merge sort** accesses data sequentially and the need of random access is low. 

refs:
- https://www.guru99.com/quicksort-in-javascript.html
- https://stackabuse.com/quicksort-in-javascript/
- https://www.geeksforgeeks.org/quick-sort/
