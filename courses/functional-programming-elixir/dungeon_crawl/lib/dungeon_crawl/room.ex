defmodule DungeonCrawl.Room do
  alias DungeonCrawl.Room
  alias DungeonCrawl.Room.Triggers
  import DungeonCrawl.Room.Action

  # A struct that contains other structs to describe the room and its actions
  defstruct description: nil, actions: [], trigger: nil

  def all, do: [
    # %Room{
    #   description: "You found a quiet place. Looks safe for a little nap.",
    #   actions: [forward(), rest()],
    # },
    %Room{
      description: "You can see the light of day. You found the exit!",
      actions: [forward()],
      trigger: Triggers.Exit
    },
    %Room{
      description: "You can see an enemy blocking your path.",
      actions: [forward()],
      trigger: Triggers.Enemy
    },
  ]
end
