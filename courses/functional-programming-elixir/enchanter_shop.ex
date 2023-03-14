defmodule EnchanterShop do

  def test_data do
  [
    %{title: "Longsword", price: 50, magic: false},
    %{title: "Healing Potion", price: 60, magic: true},
    %{title: "Rope", price: 10, magic: false},
    %{title: "Dragon's Spear", price: 100, magic: true},
  ]
  end

  @enchanter_name "Edwin"

    def enchant_for_sale([]), do: []

    # In the filter function clause, we check if an item is magical by using map pattern matching. We check if the argument contains the subset %{magic: true}. When it matches, we bind the map parameter to the variable item. Then we don’t do any item transformation; instead, we build a list where the first element is the same item, and the rest of the list is a recursive call to enchant_for_sale.
    def enchant_for_sale([item = %{magic: true} | incoming_items]) do
      [item | enchant_for_sale(incoming_items)]
    end
    def enchant_for_sale([item | incoming_items]) do
      new_item = %{
        title: "#{@enchanter_name}'s #{item.title}",
        price: item.price * 3,
        magic: true
      }
      [new_item | enchant_for_sale(incoming_items)]
    end
end
