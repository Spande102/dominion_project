from card import Card

def caravan_effect(player, game):
    player.draw_cards(1)
    player.actions += 1

    def next_turn(pl, g):
        pl.draw_cards(1)
        print(f"{pl.name} draws a card (Caravan).")
    player.add_duration("Caravan", next_turn)

Caravan = Card(
    "Caravan",
    cost=4,
    card_type=["Action", "Duration"],
    description="+1 Card +1 Action. At the start of your next turn, +1 Card.",
    effect=caravan_effect,
    expansion="seaside"
)
