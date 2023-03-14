<?php
/**
 * Fizz buzz is a group word game for children to teach them about division.
 * Players take turns to count incrementally, replacing any number divisible by three with the word "fizz",
 * and any number divisible by five with the word "buzz".
 */

/**
 * Fizz buzz (often spelled "FizzBuzz" in this context) has been used as an interview screening device for
 * computer programmers. Writing a program to output the first 100 FizzBuzz numbers is a trivial problem
 * for any would-be computer programmer, so interviewers can easily sort out those with insufficient programming ability.
 */

$i = 0; // contador
$fizzbuzz = []; // almacenador de FizzBuzzes
$ready = false;

function div3($i)
{
	return $i % 3 === 0;
}

function div5($i)
{
    return $i % 5 === 0;
}

do
{
    $i++;
    
	if (div3($i) && div5($i))
	{
		$fizzbuzz[] = $i;
	}

	if (count($fizzbuzz) === 100)
	{
		$ready = true;
	}
} while ($ready === false);

var_dump($fizzbuzz);
