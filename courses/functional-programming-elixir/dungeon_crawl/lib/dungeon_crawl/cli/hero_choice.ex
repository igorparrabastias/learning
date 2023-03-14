defmodule DungeonCrawl.CLI.HeroChoice do
  alias Mix.Shell.IO, as: Shell
  import DungeonCrawl.CLI.BaseCommands

  def start do
    Shell.cmd("clear")
    Shell.info("Start by choosing your hero:")

    heroes = DungeonCrawl.Heroes.all()

    # Anonymous function
    #  That anonymous function is necessary because we can’t use Enum.at/2 directly in the pipeline. The Enum.at/2 argument is a list, and we need to pass the hero index. The anonymous function also references the heroes variable by taking advantage of closures.
    find_hero_by_index = &Enum.at(heroes, &1)

    heroes
    # |> Enum.map(&(&1.name)) por impl de protocol
    |> display_options
    |> generate_question
    |> Shell.prompt
    |> parse_answer
    |> find_hero_by_index.()
    |> confirm_hero
  end

  defp confirm_hero(chosen_hero) do
    Shell.cmd("clear")
    Shell.info(chosen_hero.description)
    # recursive call to the start/0 function.
    if Shell.yes?("Confirm?"), do: chosen_hero, else: start()
  end
end
