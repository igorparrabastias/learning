defmodule MyList do
  @moduledoc """
  iex> MyList.filter(["a", "b", "c", "d"], &(&1 > "b"))
  #Output -> ["c", "d"]

  iex> MyList.filter([100, 200, 300, 400], &(&1 < 300))
  #Output -> [100, 200]

  iex> MyList.filter(["Alex", "Mike", "Ana"], &String.starts_with?(&1, "A"))
  #Output -> ["Alex", "Ana"]

  iex> MyList.filter(["a@b", "t.t", "a@b.c"], &String.contains?(&1, "@"))
  #Output -> ["a@b", "a@b.c"]
  """

  def each([], _function), do: nil

  def each([head | tail], function) do
    function.(head)
    each(tail, function)
  end

  # iex(10)> MyList.map([1, 4, 5], &(&1+1))
  def map([], _function), do: []

  def map([head | tail], function) do
    [function.(head) | map(tail, function)]
  end

  def reduce([], acc, _function), do: acc

  def reduce([head | tail], acc, function) do
    reduce(tail, function.(head, acc), function)
  end

  def filter([], _function), do: []

  def filter([head | tail], function) do
    if function.(head) do
      [head | filter(tail, function)]
    else
      filter(tail, function)
    end
  end
end
