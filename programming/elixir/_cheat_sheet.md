## refs
https://elixir-lang.org/crash-course.html#partials-and-function-captures-in-elixir
https://nts.strzibny.name/elixir-interactive-shell-iex/

## Tips
export ERL_AFLAGS="-kernel shell_history enabled -kernel shell_history_file_bytes 1024000"

```elixir
iex(6)> reversed = v(5) <-- Assigns value from expression at line (5) to reversed 
```

# Scopes
https://elixir-lang.readthedocs.io/en/latest/technical/scoping.html
https://groups.google.com/g/elixir-lang-talk/c/Y2FMTDEy7Dc?pli=1

## (Linked) Lists
Elixir uses square brackets to specify a list of values. Values can be of any type:

```elixir
iex> [1, 2, true, 3]
[1, 2, true, 3]
iex> length [1, 2, 3]
3
```
## Tuples
Elixir uses curly brackets to define tuples. Like lists, tuples can hold any value:

```elixir
iex> {:ok, "hello"}
{:ok, "hello"}
iex> tuple_size {:ok, "hello"}
2
```
## Keyword lists
ref: https://elixir-lang.jp/getting-started/keywords-and-maps.html

Keyword lists are a data-structure used to pass options to function.

```bash
iex> String.split("1  2  3", " ", [trim: true])
["1", "2", "3"]
```

[trim: true] is a keyword list. When a keyword list is the last argument of a function, we can skip the brackets.

```bash
iex> String.split("1  2  3", " ", trim: true)
["1", "2", "3"]
```

As the name implies, keyword lists are simply lists. In particular, they are lists consisting of 2-item tuples where the first element (the key) is an atom and the second element can be any value. Both representations are the same:

```bash
iex> [{:trim, true}] == [trim: true]
true
```

### Keyword lists as options
The characteristics of keyword lists made them the default mechanism for passing options to functions in Elixir.

When learning about if, you saw a special shorter syntax:

```elixir
if age >= 16, do: "beer", else: "no beer"
```

This may look like if accepts two arguments, but the do: and else: pair is actually a single argument - a keyword list. The same code could be written as:

```elixir
if age >= 16, [do: "beer", else: "no beer"]
# or
if age >= 16, [{:do, "beer"}, {:else, "no beer"}]
```

## Maps
Erlang R17 introduced maps, a key-value store, with no ordering. Keys and values can be any term.

```elixir
map = %{:key => 0}
map = %{map | :key => 1}
%{:key => value} = map
value === 1
#=> true
```

## Structs
https://inquisitivedeveloper.com/lwm-elixir-18/
The struct name follows the defmodule keyword, and the variables and their default values follow the defstruct keyword.
In Elixir, Structs are maps with reduced functionality, compile-time checks, and default values.
Reduced functionality means that structs cannot use protocols defined for maps like Enum, but can use functions from the Map module.
Compile-time checks ensure that structs do not have any variable that has not been declared for it, and that default values are assigned values to struct member variables if no value has been ​explicitly assigned.

## What's the meaning of "!", "?", "_", and "." syntax in elixir

! - Convention for functions which raise exceptions on failure.

? - Convention for functions which return a boolean value

_ - Used to ignore an argument or part of a pattern match expression.

. - As you mentioned is used for calling an anonymous function, but is also used for accessing a module function such as Mod.a(arg).

There does exist an important difference between variables that start with the _ (such as _foobar) and those that consist only of _ (such as def foo(_, _bar) do, _bar end). Attempts to use the _ result in compile time 'unbound variable' errors. Variables prefixed with an underscore, _bar, serve to prevent warnings for unused variables, and will not prevent compilation. Their use only generates a warning: "warning: the underscored variable "_bar" is used after being set. A leading underscore indicates that the value of the variable should be ignored..." – 

## Partials and function captures in Elixir

Elixir supports partial application of functions which can be used to define anonymous functions in a concise way:

```
Enum.map([1, 2, 3, 4], &(&1 * 2))
#=> [2, 4, 6, 8]

List.foldl([1, 2, 3, 4], 0, &(&1 + &2))
#=> 10
```

We use the same & operator to capture a function, allowing us to pass named functions as arguments.

```
defmodule Math do
  def square(x) do
    x * x
  end
end

Enum.map([1, 2, 3], &Math.square/1)
#=> [1, 4, 9]
```

# Why do we use a dot to call a function?

The dot is only used when calling anonymous functions that have been bound to a variable (and not functions defined inside a module). The dot also reminds us that it is an anonymous function.

This is an anonymous function:

> foo = fn a -> a + 1 end

And called like this:

> foo.(10)

This is a function defined inside a module:

```elixir
defmodule MyModule do
  def foo(a), do: a + 1
end
```

And called like this:

> MyModule.foo(10)

# The & Shorthand

Using anonymous functions is such a common practice in Elixir there is shorthand for doing so:

```elixir
sum = &(&1 + &2)
sum.(2, 3)
5
```

As you probably already guessed, in the shorthand version our parameters are available to us as &1, &2, &3, and so on.

# What does ~w means?

It constructs a string list. Saves you the double quotes. Also atom lists.

```elixir
~w(a b) == ["a", "b"]
~w(a b)a == [:a, :b]
```