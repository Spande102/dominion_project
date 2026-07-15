from card import Card

def shanty_town_effect(player, game):
    player.actions += 2
    print(f"{player.name} reveals their hand: {[c.name for c in player.hand]}")
    if not any("Action" in c.card_type for c in player.hand):
        player.draw_cards(2)
        print(f"{player.name} has no Action cards and draws 2 cards.")

Shanty_Town = Card(
    "Shanty Town",
    cost=3,
    card_type=["Action"],
    description="+2 Actions. Reveal your hand. If you have no Action cards in hand, +2 Cards.",
    effect=shanty_town_effect,
    expansion="intrigue"
)
