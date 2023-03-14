ref: https://hexdocs.pm/elixir/Enumerable.html

```bash
iex> Enum.each(["dogs", "cats", "flowers"], &(IO.puts String.upcase(&1)))
#Output ->
DOGS
CATS
FLOWERS

iex> Enum.map(["dogs", "cats", "flowers"], &String.capitalize/1)
#Output -> ["Dogs", "Cats", "Flowers"]

iex> Enum.reduce([10, 5, 5, 10], 0, &+/2)
#Output -> 30

iex> Enum.filter(["a", "b", "c", "d"], &(&1 > "b"))
#Output ->["c", "d"]

iex> Enum.count(["dogs", "cats", "flowers"])
#Output -> 3

iex> Enum.uniq(["a", "a", "b", "b", "b", "c"])
#Output -> ["a", "b", "c"]

iex> Enum.sum([10, 5, 5, 10])
#Output -> 30

iex> Enum.sort(["c", "b", "d", "a"], &<=/2)
#Output -> ["a", "b", "c", "d"]

iex> Enum.sort(["c", "b", "d", "a"], &>=/2)
#Output -> ["d", "c", "b", "a"]

iex> Enum.member?([10, 20, 12], 10)
#Output -> true

iex> Enum.join(["apples", "hot dogs", "flowers"], ", ") 
#Output -> "apples, hot dogs, flowers"

iex> upcase = fn {_key, value} -> String.upcase(value) end 

iex> Enum.map(%{name: "willy", last_name: "wonka"}, upcase) 
#Output -> ["WONKA", "WILLY"]

iex> medals = [
%{medal: :gold, player: "Anna"}, %{medal: :silver, player: "Joe"}, %{medal: :gold, player: "Zoe"}, %{medal: :bronze, player: "Anna"}, %{medal: :silver, player: "Anderson"}, %{medal: :silver, player: "Peter"}
]

iex> Enum.group_by(medals, &(&1.medal), &(&1.player))
#Output -> %{bronze: ["Anna"], gold: ["Anna", "Zoe"], silver: ["Joe", "Anderson", "Peter"]}
```

# Using Comprehensions

```bash
iex> for a <- ["Willy", "Anna"], b <- ["Math", "English"], do: {a, b}
#Output -> [{"Willy", "Math"}, {"Willy", "English"}, {"Anna", "Math"}, {"Anna", "English"}]

iex> parseds = for i <- ["10", "hot dogs", "20" ], do: Integer.parse(i) [{10, ""}, :error, {20, ""}]
iex> for {n, _} <- parseds, do: n
#Output -> [10, 20]

iex> for n <- [1, 2, 3, 4, 5, 6, 7], n > 3, do: n
#Output -> [4, 5, 6, 7]
```

# Infinity is constantly expanding. In Elixir, we can represent a continuously expanding collection using the higher-order function Stream.iterate/2. It creates a stream where the items are evaluated dynamically.

```bash
iex> integers = Stream.iterate(1, fn previous -> previous + 1 end) 
iex> Enum.take(integers, 5)
#Output -> [1, 2, 3, 4, 5]
```