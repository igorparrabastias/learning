defmodule FizzBuzz do
  def start(first, last) do
    first..last
    |> Enum.each(fn x -> check(x) end)
  end

  # Enum.filter([1,6,10], fn(number) -> number > 5 end)
  # Could be re-written as:
  #
  # Enum.filter([1,6,10], &(&1 > 5))

  defp check(number) when rem(number, 15) == 0, do: IO.puts("FizzBuzz")
  defp check(number) when rem(number, 3) == 0, do: IO.puts("Fizz")
  defp check(number) when rem(number, 5) == 0, do: IO.puts("Buzz")
  defp check(number), do: IO.puts("#{number}")
end
