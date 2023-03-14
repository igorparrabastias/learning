# defmodule Factorial do
#   def of(0), do: 1
#   def of(1), do: 1
#   def of(2), do: 2 * 1
#   def of(3), do: 3 * 2 * 1
#   def of(4), do: 4 * 3 * 2 * 1
# end

# defmodule Factorial do
#   def of(0), do: 1
#   def of(1), do: 1 * of(0)
#   def of(2), do: 2 * of(1)
#   def of(3), do: 3 * of(2)
#   def of(4), do: 4 * of(3)
# end

defmodule Factorial do
  def of(0), do: 1
  def of(n) when n > 0, do: n * of(n - 1)
end
