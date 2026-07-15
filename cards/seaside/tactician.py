from card import Card

def tactician_effect(player, game):
    if not player.hand:
        print("No cards to discard - Tactician does nothing.")
        return
    n = len(player.hand)
    player.discard_pile.extend(player.hand)
    player.hand = []
    print(f"{player.name} discards their hand ({n} cards).")

    def next_turn(pl, g):
        pl.draw_cards(5)
        pl.actions += 1
        pl.buys += 1
        print(f"{pl.name} gets +5 Cards +1 Action +1 Buy (Tactician).")
    player.add_duration("Tactician", next_turn)

Tactician = Card(
    "Tactician",
    cost=5,
    card_type=["Action", "Duration"],
    description="Discard your hand. If you discarded any cards this way, then at the start of your next turn, +5 Cards, +1 Action, and +1 Buy.",
    effect=tactician_effect,
    expansion="seaside"
)
