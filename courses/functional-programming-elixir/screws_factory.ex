defmodule ScrewsFactory do
  def run(pieces) do
    pieces
    # |> Enum.map(&add_thread/1)
    # |> Enum.map(&add_head/1)
    # |> Enum.each(&output/1)
    # We use the Stream.map/1 at the beginning of the pipeline to create a stream.
    |> Stream.map(&add_thread/1)
    |> Stream.map(&add_head/1)
    |> Enum.each(&output/1)
  end

  defp add_thread(piece) do
    Process.sleep(50)
    piece <> "--"
  end

  defp add_head(piece) do
    Process.sleep(100)
    "o" <> piece
  end

  defp output(screw) do
    IO.inspect(screw)
  end
end
