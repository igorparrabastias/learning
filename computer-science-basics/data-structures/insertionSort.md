# Insertion sort

**Insertion sort** is a simple sorting algorithm that works similar to the way you sort playing cards in your hands. The array is virtually split into a sorted and an unsorted part. Values from the unsorted part are picked and placed at the correct position in the sorted part.

This algorithm is one of the simplest algorithm with simple implementation. Is adaptive in nature, i.e. it is appropriate for data sets which are already partially sorted.

## Advantages
- Implementation of insertion sort is very easy as compared to sorting algorithms like quick sort, merge sort or heap sort.
- Very efficient in the case of a small number of elements.
- If the elements are already in sorted order it won’t spend much time in useless operations and will deliver a run time of O(n).
- It is more efficient when compared to other simple algorithms like Bubble sort and Selection Sort.
- It is a stable sorting technique, that is, the order of keys is maintained.
- It requires constant “additional” memory, no matter the number of elements.
- It can sort the elements as soon as it receives them.
- It can turn out to be very efficient in case of nearly sorted elements.
## Disadvantages
- One of the major disadvantages of Insertion sort is its Average Time Complexity of O(n^2).
- If the number of elements is relatively large it can take large time as compared to Quick Sort or Merge Sort.

## Complexity
- Time Complexity: O(N^2) 
- Auxiliary Space: O(1). We have three constant variables, temp, j and i. One could argue that you would have to store the array in memory, which gives O(n).

## When is the Insertion Sort algorithm used?
- **Insertion sort** is used when number of elements is small. It can also be useful when input array is almost sorted, only few elements are misplaced in complete big array.

refs: 
- https://www.geeksforgeeks.org/insertion-sort/
- https://tutswiki.com/data-structures-algorithms/insertion-sort/