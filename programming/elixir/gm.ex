defmodule Gm do
  def print(option) do
    option
    |> g
    |> IO.puts()
  end

  defp g(opt) do
    cond do
      opt == 1 -> "Hello"
      opt == 2 -> "Hello, World"
      true -> "Hello planet Earth"
    end
  end
end
