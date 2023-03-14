defmodule Halloween do
  def give_candy(kids) do
    ~w(chocolate jelly mint xxx)
    |> Stream.cycle
    # https://superruzafa.github.io/visual-elixir-reference/Enum/zip/1/
    #  When we zip them together, the function will stop combining them when it reaches the end of the shorter list.
    |> Enum.zip(kids)
  end
end
