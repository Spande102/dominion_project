from card import Card

def magnate_effect(player, game):
    print(f"{player.name} reveals their hand: {[c.name for c in player.hand]}")
    treasures = sum(1 for c in player.hand if "Treasure" in c.card_type)
    player.draw_cards(treasures)
    print(f"{player.name} draws {treasures} card(s) (one per Treasure).")

Magnate = Card(
    "Magnate",
    cost=5,
    card_type=["Action"],
    description="Reveal your hand. +1 Card per Treasure in it.",
    effect=magnate_effect,
    expansion="prosperity"
)
