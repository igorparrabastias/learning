/**
1. Top-down with Memoization

It is by far the more famous of the two. In this approach, 
we try to solve the bigger problem by recursively finding 
the solution to smaller sub-problems. Whenever we solve a 
sub-problem, we store its result so that we don’t end up 
solving it repeatedly if it’s called multiple times (like 
it is in the Fibonacci function). Instead, we can just 
look up and return the saved result. This technique of 
storing the results of already solved subproblems is 
called Memoization.

Why is it called the top-down approach?

We start with the given n and then recursively calculate 
fib(n-1) + fib(n-2) until we reach the base case. That is 
when we can start returning out results and “hand-them 
over” to our consecutive calls (that have been waiting on 
the stack, btw) until they all return a number and fib(n) 
can be calculated and returned as well.
*/

const fibWithMemo = n => {
  let memo = {} // we will store("memoize") our values here

  const fib = (n) => {
    let value

    if (n in memo) {
      // if the n is already in our memo object, we look it up and store it in value
      value = memo[n]
    } else {
      // otherwise, we calculate it and store it in value
      if (n === 1 || n === 2) {
        value = 1
      } else {
        value = fib(n - 1) + fib(n - 2)
      }
      // store the value for current n to our memo object
      memo[n] = value
    }
    console.log(memo)
    return value
  }
  return fib(n)
}

/*
As we saw above, this problem shows the overlapping 
subproblems pattern, so let’s make use of memoization 
here. We can use an object (you could also use an array 
and store the values at the index corresponding to the 
current n)array to store the already solved subproblems. 
Memoization assures that each subproblem (each fib(n)) 
is calculated at most once.
*/

/*
2. Bottom - up with Tabulation

Tabulation is the opposite of the top - down approach and 
avoids recursion.Why would we want to do that ? Recursion 
is elegant and memoization makes it immensely more 
efficient, however, storing the results in the way 
memoization does can be very expensive in terms of space 
and storage.Tabulation’s time complexity is similar to 
recursion with memorization.Its space complexity tends to 
be much better though.

In this approach, we solve the problem “bottom - up” (i.e.
by solving all the related sub - problems first). This 
is typically done by filling up an n - dimensional table
(hence the term “tabulation”).Based on the results in 
the table, the solution to the top / original problem is 
then computed.

Tabulation is the opposite of Memoization, and is usually 
implemented with iteration(loops) — start with the base 
case and move forward from there.Just as in Memoization we 
solve the problem and maintain a map of already solved 
sub-problems.In other words, in memoization, we do it 
top-down in the sense that we solve the top problem first
(which then typically recurses down to solve the sub - 
problems).
*/

const fibWithTab = n => {
  if (n === 1 || n === 2) return 1
  // initialize an array and store the values we already know
  let fibNums = [0, 1, 1]
  // loop starting at index 3 (first value we do not know) until n
  for (let i = 3; i <= n; i++) {
    // store values in the array at Nth index
    fibNums[i] = fibNums[i - 1] + fibNums[i - 2]
  }
  return fibNums[n]
}

/*
To sum up — dynamic programming is a flavor of programming
that can be used with some very specific problems that
share two characteristics — they can be broken down into
smaller sub - problems that are not unique and often
shared, and the best solution for the problem will consist
of best possible solutions for the sub - problems.
*/

// credits: https://medium.com/swlh/demystifying-dynamic-programming-b22d65095866