defmodule SecretHandshake do
  @doc """
  Determine the actions of a secret handshake based on the binary
  representation of the given `code`.

  If the following bits are set, include the corresponding action in your list
  of commands, in order from lowest to highest.

  1 = wink
  10 = double blink
  100 = close your eyes
  1000 = jump

  10000 = Reverse the order of the operations in the secret handshake
  Son 32 posibles combinaciones
  """

  def check_code(bin, index) do
    if(
      Enum.at(bin, index) == 1,
      do:
        case index do
          0 -> ["wink"]
          1 -> ["double blink"]
          2 -> ["close your eyes"]
          3 -> ["jump"]
          4 -> true
          _ -> nil
        end,
      else: nil
    )
  end

  @spec commands(code :: integer) :: list(String.t())
  def commands(code) do
    bin = Enum.reverse(Integer.digits(code, 2))
    bin2 = Enum.with_index(bin)

    Enum.reduce(bin2, [], fn {_, index}, acc ->
      x = check_code(bin, index)

      if x === true do
        Enum.reverse(acc)
      else
        if(x, do: acc ++ x, else: acc)
      end
    end)

    # |> IO.inspect()
  end
end

# SecretHandshake.commands(31_00000000000000000000027)
