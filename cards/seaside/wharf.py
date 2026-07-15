from card import Card

def wharf_effect(player, game):
    player.draw_cards(2)
    player.buys += 1

    def next_turn(pl, g):
        pl.draw_cards(2)
        pl.buys += 1
        print(f"{pl.name} gets +2 Cards +1 Buy (Wharf).")
    player.add_duration("Wharf", next_turn)

Wharf = Card(
    "Wharf",
    cost=5,
    card_type=["Action", "Duration"],
    description="Now and at the start of your next turn: +2 Cards +1 Buy.",
    effect=wharf_effect,
    expansion="seaside"
)
