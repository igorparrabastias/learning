// Program to count down numbers to 1
function countDown(number) {

  // display the number
  console.log(number);

  // decrease the number value
  const newNumber = number - 1;

  // base case
  if (newNumber > 0) {
    countDown(newNumber);
  }
}

// Program to find the factorial of a number
function factorial(x) {

  // if number is 0
  if (x === 0) {
    return 1;
  }

  // if number is positive
  else {
    return x * factorial(x - 1);
  }
}

const fibonacci = (n) => (n <= 2 ? 1 : fibonacci(n - 1) + fibonacci(n - 2));

function test() {
  countDown(10);

  const num = 3;
  console.log(`${num}! is ${factorial(num)}`);

  console.log(fibonacci(10));

}