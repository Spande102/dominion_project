from card import Card

def pirate_effect(player, game):
    # Simplification: the official on-Treasure-gain reaction play is not
    # implemented; Pirate simply delivers its Gold next turn.
    def next_turn(pl, g):
        if pl.gain_card(g, g.find_supply_pile("Gold"), destination='hand'):
            print(f"{pl.name} gains a Gold to their hand (Pirate).")
    player.add_duration("Pirate", next_turn)

Pirate = Card(
    "Pirate",
    cost=5,
    card_type=["Action", "Duration", "Reaction"],
    description="At the start of your next turn, gain a Gold to your hand.",
    effect=pirate_effect,
    expansion="seaside"
)
