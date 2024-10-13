# Data structures and algorithms in javascript

## Complex Sort Algorithms
Larger data sets require more complex code and more memory. The **quick sort** and **heap sort** both split and copy the data sets to optimize the number of comparisons. The **quick sort** continually divides the list then reassembles it in sorted order. The **heap sort** copies the data into a tree structure then traverses the tree to copy the data back into order. Both are fast and efficient but take more code and much more working storage. Choose these algorithms for large data sets.

## Animations
- Quick sort v/s Bubble sort: https://youtu.be/aXXWXz5rF64
- Merge sort v/s Quick sort: https://youtu.be/es2T6KY45cA
- Insertion Sort v/s Bubble Sort: https://youtu.be/TZRWRjq2CAg

refs:
- https://www.techwalla.com/articles/how-to-sort-a-row-or-column-in-excel

# Arrays

## Static arrays
- The size or length of this type of array is determined at compile time (before run time), that is you have to specify the number of indices you want in that array. This type of array is only applicable in low-level languages like C++:
- If we need to append a new value into the array, we will have to create a new array and state its new size. The memory is already determined in the RAM.
- People have come to say that one of the reasons why C++ is faster is because it does not just create unused memory.

refs:  
- https://blog.sessionstack.com/how-javascript-works-arrays-vs-hash-tables-ab769bf84a2d

# Backtracking

refs:   
- https://betterprogramming.pub/the-technical-interview-guide-to-backtracking-e1a03ca4abad
- https://www.geeksforgeeks.org/backtracking-introduction/

# Binary Search

- Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one.
- Binary search is the most efficient searching algorithm having a run-time complexity of O(log2 N) in a sorted array.
- Binary search begins by comparing the middle element of the list with the target element. If the target value matches the middle element, its position in the list is returned. If it does not match, the list is divided into two halves. The first half consists of the first element to the middle element whereas the second half consists of the element next to the middle element to the last element i.e. the search interval is repeatedly divided into halves.

refs:
- https://www.interviewbit.com/courses/programming/binary-search/


# Binary search tree

- BST is a tree-like data structure with a single root at the very top. They are a great way to store numeric values as their ordered nature allows for fast search and lookups.
- Binary search tree is ordered/sorted data structure, upon insertion, the nodes are placed in an orderly fashion. This inherent order makes searching fast. 

## Properties
- Every left child has a smaller value than its parent
- Every right child has a larger value than its parent
- ie: left child < parent node < right child
- Every node can contain from 0 to 2 children.
- Like all tree data structure, binary search tree has a root, the top node

## Balanced vs unbalanced
- With a balanced tree, access (lookup, insert, and remove operations) is O(log n).
- With an unbalanced tree, access1 is O(n) (worst case).

## Complexity
- Average: The number of items is split in half, as we decide whether to go for the left subtree, or right subtree.
- Worst: If the tree is very unbalanced, it resembles a linked list.
- Worst space: The more items, the bigger the data list.

refs:  
- https://www.educative.io/courses/mastering-data-structures-and-sorting-algorithms-in-javascript/qV2DzMZ514r
- https://www.geeksforgeeks.org/implementation-binary-search-tree-javascript/
- https://stackoverflow.com/questions/59206128/balanced-vs-unbalanced-binary-tree-clarification-needed
- https://baffinlee.com/leetcode-javascript/problem/balanced-binary-tree.html

# Dynamic Programming

- Dynamic Programming is mainly an optimization over plain recursion. Wherever we see a recursive solution that has repeated calls for same inputs, we can optimize it using Dynamic Programming. The idea is to simply store the results of subproblems, so that we do not have to re-compute them when needed later. This simple optimization reduces time complexities from exponential to polynomial.  
For example, if we write simple recursive solution for Fibonacci Numbers, we get exponential time complexity and if we optimize it by storing solutions of subproblems, time complexity reduces to linear.
- An algorithmic approach is used to optimize a naive solution (usually recursive) by storing calculations in memory and reusing them when needed to save time.
- The basis of dynamic programming is to calculate each subproblem only once and save the result for later if it needs to recalculate again.
---
-  Some might say that dynamic programming and recursion with memoization are one and the same but it is not technically correct.
- Dynamic programming is a broader term — an approach to solve some problems, a small subset, but those we can apply this approach to can speed up the code dramatically.

## Conditions
Overlapping subproblems:
- The problem is recursive and thus can be broken down into subproblems
- The sub-problems will usually overlap at some point.

Optimal substructure:
- A problem is said to have an optimal substructure if the optimal solution (best solution) can be constructed from optimal solutions of its subproblems. Once again, Fibonacci is a good example of such a problem. Another good example is finding the shortest path between two points.


## Dynamic programming problems can be solved using 2 approaches

- Bottom Up Dynamic programming: In this approach, we first analyze the problem and see the order in which the sub-problems are solved.We start by solving the trivial sub problem and build up towards the given problem.
- Top Down Dynamic Programming: In this approach, we start solving the given problem by breaking it down. If you see that a given sub problem has been solved already, then just return the stored solution.

## Difference Between Greedy Method and Dynamic Programming

### Greedy algorithm
It is an algorithmic paradigm that builds up on a solution in parts, step by step. The next step is chosen such that it gives the most obvious and immediate benefit.

- Problems that involve choosing local optimal values will help in choosing the global optimal values/solution to the problem. Such ate the problems associated with greedy algorithm.
- There is no surety that a greedy algorithm would lead to an optimal solution.
- An optimal choice is made at every stage of the problem, i.e the local optimal solution.
- It is efficient in terms of memory usage since there is no question of having to go back or change previous solutions/values.
- In general, they are quick in comparison to dynamic programming techniques.
- Example: Dijkstra's shortest path algorithm that takes O(ELogV + VLogV) time.
- The solution in a greedy algorithm is computed in a forward method, never visiting the previous values/solutions or changing them.

### Dynamic Programming
It is an optimization technique that helps store the result of sub-problems so that they don't need to be re-computed when need in the future. They can just be extracted from the pre-computed set. It reduces the time complexity from exponential to polynomial complexity. 

- For example: A recursive solution can be turned into a dynamic programming problem by computing.
- In this, the decision made at every step is done by considering the current problem in hand, and the solution to previously solved sum-problem. This will be used to calculate the optimal value/solution.
- It is guaranteed that a dynamic programming problem's solution would be an optimal one.
- Here, the optimal solution chosen is a globally optimal one. It uses certain formula which would have been used to store previously calculated state values.
- The dynamic programming table is required for memorization. This increases the memory complexity.
- It is comparatively slower.
- Example: Bellman Ford algorithm that takes O(VE) time.
- Dynamic programming determines the solution using a bottom up or top down approach, by developing from smaller problems that have optimal solutions.

## Case: Fibonacci

This naive implementation has complexity O(2^n) ie. Growth doubles with each additon to the input data set. 

```c
int fibonacci(int n) {
  if (n == 1 || n == 2) return 1;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

```
Algorithms with running time O(2^N) are often recursive algorithms that solve a problem of size N by recursively solving two smaller problems of size N-1.

## Memoization vs. Tabulation
We mentioned earlier that dynamic programming is a technique for solving problems by breaking them down into smaller subsets of the same problem (using recursion). To solve problems using dynamic programming, there are two approaches that we can use, memoization and tabulation

The idea of 'storing' the result of an expensive function (fib) is known as memoization. Memoization is implemented by maintaining a lookup table of previous solved sub-problems. This approach is also known as "top down" since you solve the solve the "top" problem first (which typically recurses down to solve the sub-problems).

When you solve a dynamic programming problem using tabulation you solve the by solving all related sub-problems first. This means that you must decide in which order to solve your sub-problems first, which adds another step, but gives you more flexibility than memoization. This approach is traditionally known as a "bottom up" approach since the sub-problems are calculated first. 

## Fibonacci With Dynamic Programming
Problem: The naive Fibonacci implementation recomputes two values of Fibonacci that we have already computed.

Solution: Use dynamic programming along with memoization to save values in a hash in order to not have to recompute values that have already been computed.

Below is the dynamic programming solution that uses memoization (done with an object) to store the values of fib(n). If the values are needed again, they can be looked up using savedFib without having to recompute them.

```js
function fib(n, savedFib={}) {
   // base case
   if (n <= 0) { return 0; }
   if (n <= 2) { return 1; }

   // memoize
   if (savedFib[n - 1] === undefined) {
        savedFib[n - 1] = fib(n - 1, savedFib);
   }

   // memoize
   if (savedFib[n - 2] === undefined) {
        savedFib[n - 2] = fib(n - 2, savedFib);
   }

   return savedFib[n - 1] + savedFib[n - 2];
}
```
Here is a solution to the same Fibonnaci problem using tabulation.

```js
function fib(n){
    // array declaration - notice that we figure out how many elements will be here before the calculations begin. This is the 'tabulation' approach so let's make a new array and fill it with 0s
    var arr = new Array(n+1).fill(0)
    // base case assignment
    arr[1] = 1;
    // calculating the fibonacci and storing the values
    for(var i = 2; i <= n; i++){
      arr[i] = arr[i-1] + arr[i-2]
    }
    return arr[n]
}
```

It's important to understand that both of these options can be used to solve dynamic programming problems so they are not mutually exclusive.

refs: 
- https://www.geeksforgeeks.org/dynamic-programming/
- https://evoniuk.github.io/posts/fibonacci.html
- https://www.tutorialspoint.com/dynamic-programming-in-javascript
- https://medium.com/swlh/demystifying-dynamic-programming-b22d65095866
- https://medium.com/swlh/javascript-recursion-and-memoization-for-dummies-fd23564201b7
- https://www.tutorialspoint.com/difference-between-greedy-method-and-dynamic-programming
- https://www.rithmschool.com/courses/javascript-computer-science-fundamentals/dynamic-programming

# Graphs

The graph is a non-linear data structure. Graph G contains a set of vertices V and a set of Edges E. Graph has lots of applications in computer science. 

Graph is basically divided into two broad categories : 
- Directed Graph (Di- graph) – Where edges have direction.
- Undirected Graph – Where edges do not represent any directed

There are various ways to represent a Graph:- 
- Adjacency Matrix
- Adjacency List

BFS
- Time Complexity: O(V+E), where V is the number of nodes and E is the number of edges.
- Auxiliary Space: O(V)

DFS
- Time Complexity:  O(V + E), where V is the number of vertices and E is the number of edges in the graph.
- Auxiliary Space: O(V), since an extra visited array of size V is required.

refs:  
- https://www.geeksforgeeks.org/implementation-graph-javascript/
- https://adrianmejia.com/data-structures-for-beginners-graphs-time-complexity-tutorial/

# Hash tables
Hash tables are powerful data structures in the field of computing. Data structures and algorithms are known for solving problems effectively. Hash tables access components in constant time (O(1)). Hash tables enable us to find data quickly using keys.

## Hash tables vs. trees
- Trees are more useful when an application needs to order data in a specific sequence. Hash tables are the smarter choice for randomly sorted data due to its key-value pair organization.
- Hash tables can perform in constant time, while trees usually work in O(log n). In the worst-case scenario, the performance of hash tables can be as low as O(n)
- An AVL tree, however, would maintain O(log n) in the worst case.

## Common hash functions
There are many kinds of hash functions that have different uses. Let’s take a look at some of the most common hash functions used in modern programming.
- Arithmetic Modular: In this approach, we take the modular of the key with the list/array size: index=key MOD tableSize. So, the index will always stay between 0 and tableSize - 1.
- Truncation: Here, we select a part of the key as the index rather than the whole key. We can use a mod function for this operation, although it does not need to be based on the array size
- Folding: This approach involves dividing the key into small chunks and applying a different arithmetic strategy at each chunk.

## Handling collisions
Collisions occur when different keys get hashed to the same number or index.
How can we resolve this issue? There are many methods of handling collisions. We will learn a few below.
- Separate chaining: Separate chaining is a method which key-value pairs hash to the same index in the bucket array. A linked list is created for that particular index.
In this strategy, you have to iterate between the pairs to find the key you are looking for. Separate chaining leads to inefficiency. It brings the time complexity closer to O(n). Meaning it depends linearly on the size of the input.
- Linear probing: In linear probing, you add one element and move to the next position if the hashed index is available.
- Rehashing: Rehashing is re-calculating the hash value of the stored key-value pairs. Then moving them to a bigger hash map when the threshold is reached.

refs: 
- https://www.educative.io/blog/data-strucutres-hash-table-javascript
- https://www.section.io/engineering-education/hash-tables-in-javascript/
- https://www.mattzeunert.com/2017/02/01/implementing-a-hash-table-in-javascript.html

# Linked lists

A singly linked list is a linear data structure. Each element, called a node, is connected to the other, by pointers (or references) to the next node.

LinkedList is the dynamic data structure, as we can add or remove elements at ease, and it can even grow as needed. Just like arrays, linked lists store elements sequentially, but don’t store the elements contiguously like an array. 

## Complexity
- Get, Search, Insertion and Deletion: To get to a node in the list, we would have to walk through the list to find the node we’re searching. It is possible to use pointers instead, which would be constant, but in these examples, the time complexity would be linear.
- Worst space: The more items, the bigger the list.

refs: 
- https://www.educative.io/courses/mastering-data-structures-and-sorting-algorithms-in-javascript/7npNQEZK318
- https://www.geeksforgeeks.org/implementation-linkedlist-javascript/

# Queues

You can think of a queue as a pipe, with both ends open. Objects enter from one and are removed from the other. This means that, unlike the stack that used the last-in-first-out principle, queues use the first-in-first-out principle.

A Queue works on the FIFO(First in First Out) principle. Hence, it performs two basic operations that is addition of elements at the end of the queue and removal of elements from the front of the queue. Like Stack, Queue is also a linear data structure.
Note: Assuming a queue can grow dynamically we are not considering the overflow condition

## Complexity
- Get and Search: To get or search for a certain value, we’d have to walk over all the items in the queue. The time needed is directly proportional to the number of items in the queue.
- Insertion: When we insert new data into the queue, we push it to the end of the queue.
- Deletion: Due to the internals of the JavaScript shift method, which walks over the entire array and returns the last item, the time complexity for deletion is linear.
- Worst space: The more items, the bigger the queue array.

refs:
- https://www.educative.io/courses/mastering-data-structures-and-sorting-algorithms-in-javascript/B8r6jD5NO5N

# Recursion

Recursion is a widely used phenomenon in computer science used to solve complex problems by breaking them down into simpler ones. Recursion is a process by which a function calls itself directly or indirectly. The corresponding function is called as recursive function.

Using recursive algorithms, certain complex problems can be solved quite easily.

## What is a base condition in recursion?
In a recursive function, the solution to the base case is provided and the solution of the bigger problem is expressed in terms of smaller problems.

The role of the base condition is to stop a recursive function from executing endlessly – once a pre-specified base condition is met, the function knows it’s time to exit.

To prevent infinite recursion, you can use if...else statement (or similar approach) where one branch makes the recursive call, and the other doesn't.

So, it generally looks like this.

```js
function recurse() {
    if(condition) {
        // stop calling itself
        //...
    } else {
        recurse();
    }
}

recurse();
```


## Two ways of thinking
For something simple to start with – let’s write a function pow(x, n) that raises x to a natural power of n. In other words, multiplies x by itself n times.

```
pow(2, 2) = 4
pow(2, 3) = 8
pow(2, 4) = 16
```

There are two ways to implement it.

Iterative thinking: the for loop:

```js
function pow(x, n) {
  let result = 1;

  // multiply result by x n times in the loop
  for (let i = 0; i < n; i++) {
    result *= x;
  }

  return result;
}

alert( pow(2, 3) ); // 8
```

Recursive thinking: simplify the task and call self:

```js
function pow(x, n) {
  if (n == 1) {
    return x;
  } else {
    return x * pow(x, n - 1);
  }
}

alert( pow(2, 3) ); // 8
```

Please note how the recursive variant is fundamentally different.

When pow(x, n) is called, the execution splits into two branches:

```
              if n==1  = x
             /
pow(x, n) =
             \
              else     = x * pow(x, n - 1)
```

- If n == 1, then everything is trivial. It is called the base of recursion, because it immediately produces the obvious result: pow(x, 1) equals x.
- Otherwise, we can represent pow(x, n) as x * pow(x, n - 1). In maths, one would write xn = x * xn-1. This is called a recursive step: we transform the task into a simpler action (multiplication by x) and a simpler call of the same task (pow with lower n). Next steps simplify it further and further until n reaches 1.

## InternalError: too much recursion
The JavaScript exception "too much recursion" or "Maximum call stack size exceeded" occurs when there are too many function calls, or a function is missing a base case.

### Message

```
RangeError: Maximum call stack size exceeded (Chrome)
InternalError: too much recursion (Firefox)
RangeError: Maximum call stack size exceeded. (Safari)
```

### What went wrong?   

A function that calls itself is called a recursive function. Once a condition is met, the function stops calling itself. This is called a base case.

In some ways, recursion is analogous to a loop. Both execute the same code multiple times, and both require a condition (to avoid an infinite loop, or rather, infinite recursion in this case). When there are too many function calls, or a function is missing a base case, JavaScript will throw this error.

## The execution context and stack
Now let’s examine how recursive calls work. For that we’ll look under the hood of functions.

The information about the process of execution of a running function is stored in its execution context.

The execution context is an internal data structure that contains details about the execution of a function: where the control flow is now, the current variables, the value of this (we don’t use it here) and few other internal details.

One function call has exactly one execution context associated with it.

When a function makes a nested call, the following happens:

The current function is paused.
The execution context associated with it is remembered in a special data structure called execution context stack.
The nested call executes.
After it ends, the old execution context is retrieved from the stack, and the outer function is resumed from where it stopped.

refs:
- https://www.educative.io/answers/what-is-recursion
- https://javascript.info/recursion
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Too_much_recursion
- https://www.programiz.com/javascript/recursion
- https://developer.mozilla.org/en-US/docs/Glossary/Recursion

# Stacks

Stack is a very useful data structure and has a wide range of application. Stack is a linear data structure in which addition or removal of element follows a particular order i.e. LIFO(Last in First Out) AND FILO(First in Last Out).  
Note : Assuming the stack can grow dynamically (in javascript) we are not considering the overflow condition.

You can think of the stack as a container, to which we can add items, and remove them. Only the top of this “container” is open, so the item we put in first will be taken out last, and the items we put in last will be taken out first. This is called the last-in-first-out principle.

## Applications of the stack:
- Infix to Postfix /Prefix conversion
- Redo-undo features at many places like editors, photoshop.
- Forward and backward features in web browsers
- Used in many algorithms like Tower of Hanoi, tree traversals, stock span problems, and histogram problems.
- Backtracking is one of the algorithm designing techniques. Some examples of backtracking are the Knight-Tour problem, N-Queen problem, find your way through a maze, and game-like chess or checkers in all these problems we dive into someway if that way is not efficient we come back to the previous state and go into some another path. To get back from a current state we need to store the previous state for that purpose we need a stack.
- In Graph Algorithms like Topological Sorting and Strongly Connected Components
- In Memory management, any modern computer uses a stack as the primary management for a running purpose. Each program that is running in a computer system has its own memory allocations
- String reversal is also another application of stack. Here one by one each character gets inserted into the stack. So the first character of the string is on the bottom of the stack and the last element of a string is on the top of the stack. After Performing the pop operations on the stack we get a string in reverse order.

Implementation of Stack: There are two ways to implement a stack
- Using array
- Using linked list

## Complexity
- Get and Search: To get or search for a certain value, we’d have to walk over all the items in the stack. The amount of time needed is directly proportional to the number of items in the stack.
- Insertion and Deletion: When we insert new data onto the stack, we add it at the top of the stack. When we delete an item, we pop the top element off. No need to iterate through any data.
- Worst space: The more items, the bigger the stack array.

refs: 
- https://www.geeksforgeeks.org/implementation-stack-javascript/

# Dijkstra’s Algorithm to find the shortest path between vertices in a graph.

refs:
- https://reginafurness.medium.com/dijkstras-algorithm-in-javascript-4b5db48a93d4