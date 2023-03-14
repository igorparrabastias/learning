# Partial applications

defmodule WordBuilder do
  def build(alphabet, positions) do
    #  use the function-capturing syntax
    letters = Enum.map(positions, &String.at(alphabet, &1))
    Enum.join(letters)
  end

    def build2(alphabet, positions) do
    # We took advantage of closures, referencing the alphabet variable, making our anonymous function remember its value.
    partial = fn at -> String.at(alphabet, at) end
    letters = Enum.map(positions, partial)
    Enum.join(letters)
  end
end

range = 1..10 # lazy coll
Enum.each(range, &IO.puts/1) # Solo aqui se evalua
