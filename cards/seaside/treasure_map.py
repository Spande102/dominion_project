from card import Card

def treasure_map_effect(player, game):
    this = next((c for c in player.in_play if c.name == "Treasure Map"), None)
    if this:
        player.in_play.remove(this)
        game.trash_pile.append(this)
        print(f"{player.name} trashes the played Treasure Map.")
    other = next((c for c in player.hand if c.name == "Treasure Map"), None)
    if this and other:
        player.hand.remove(other)
        game.trash_pile.append(other)
        print(f"{player.name} trashes a second Treasure Map!")
        for _ in range(4):
            player.gain_card(game, game.find_supply_pile("Gold"), destination='deck')
        print(f"{player.name} gains 4 Golds onto their deck.")
    else:
        print("No second Treasure Map in hand - nothing happens.")

Treasure_Map = Card(
    "Treasure Map",
    cost=4,
    card_type=["Action"],
    description="Trash this and a Treasure Map from your hand. If you trashed 2 Treasure Maps, gain 4 Golds onto your deck.",
    effect=treasure_map_effect,
    expansion="seaside"
)
