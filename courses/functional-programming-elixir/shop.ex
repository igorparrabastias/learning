defmodule Shop do
  # def checkout(price) do
  #   case ask_number("Quantity?") do
  #     :error -> IO.puts("It's not a number")
  #     {quantity, _} -> quantity * price
  #   end
  # end

  # def ask_number(message) do
  #   message <> "\n"
  #     |> IO.gets
  #     |> Integer.parse
  # end

  # # version 2
  # def checkout() do
  #   case ask_number("Quantity?") do
  #     :error ->
  #       IO.puts("It's not a number")
  #     {quantity, _} ->
  #       case ask_number("Price?") do
  #         :error ->
  #           IO.puts("It's not a number")
  #         {price, _} ->
  #           quantity * price
  #       end
  #   end
  # end

  # def ask_number(message) do
  #   message <> "\n"
  #     |> IO.gets
  #     |> Integer.parse
  # end

  # version 3
  def checkout() do
    quantity = ask_number("Quantity?")
    price = ask_number("Price?")
    calculate(quantity, price)
  end

  def calculate(:error, _), do: IO.puts("Quantity is not a number")
  def calculate(_, :error), do: IO.puts("Price is not a number")
  def calculate({quantity, _}, {price, _}), do: quantity * price

  def ask_number(message) do
    message <> "\n"
      |> IO.gets
      |>
  end
end
