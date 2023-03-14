defmodule ScrewsFactory do
  def run(pieces) do
    pieces
    # The chunk function is responsible for accumulating some items before sending them to the next function. It creates a queue in our processing pipeline.
    # Ex: Enum.chunk([1, 2, 3, 4, 5, 6], 2)
    |> Stream.chunk(50)
    # Ex: Enum.flat_map([[1, 2], [3, 4], [5, 6]], &(&1))
    # Es como procesar por lotes
    |> Stream.flat_map(&add_thread/1)
    |> Stream.chunk(100)
    |> Stream.flat_map(&add_head/1)
    |> Enum.each(&output/1)
  end

  defp add_thread(pieces) do
    Process.sleep(50)
    Enum.map(pieces, &(&1 <> "--"))
  end

  defp add_head(pieces) do
    Process.sleep(100)
    Enum.map(pieces, &("o" <> &1))
  end

  defp output(screw) do
    IO.inspect(screw)
  end
end
