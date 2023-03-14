# defmodule NucleotideCount do
#   # @nucleotides [?A, ?C, ?G, ?T]
#
#   @doc """
#   Counts individual nucleotides in a NucleotideCount strand.
#
#   ## Examples
#
#   iex> NucleotideCount.count('AATAA', ?A)
#   4
#
#   iex> NucleotideCount.count('AATAA', ?T)
#   1
#   """
#   @spec count([char], char) :: non_neg_integer
#   def count(strand, nucleotide) do
#     strand
#     |> to_string
#     |> String.graphemes()
#     |> Enum.filter(fn x -> x == <<nucleotide>> end)
#     # |> Enum.reduce(0, fn x, acc -> 1 + acc end)
#
#     |> Enum.count()
#   end
#
#   @doc """
#   Returns a summary of counts by nucleotide.
#
#   ## Examples
#
#   iex> NucleotideCount.histogram('AATAA')
#   %{?A => 4, ?T => 1, ?C => 0, ?G => 0}
#   """
#   @spec histogram([char]) :: map
#   def histogram(strand) do
#     %{
#       ?A => count(strand, ?A),
#       ?T => count(strand, ?T),
#       ?C => count(strand, ?C),
#       ?G => count(strand, ?G)
#     }
#   end
# end

defmodule NucleotideCount do
  @nucleotides [?A, ?C, ?G, ?T]

  @spec count([char], char) :: non_neg_integer
  def count(strand, nucleotide) do
    Enum.reduce(strand, 0, fn x, acc ->
      if(x == nucleotide, do: acc + 1, else: acc)
    end)
  end

  @spec histogram([char]) :: map
  def histogram(strand) do
    Enum.reduce(@nucleotides, %{}, fn x, acc ->
      Map.merge(acc, %{x => count(strand, x)})
    end)

    # Enum.reduce(@nucleotides, %{}, fn el, acc ->
    #   count = count(strand, el)
    #   Dict.put(acc, el, count) # Dict.put deprecated!!!
    # end)
  end
end
