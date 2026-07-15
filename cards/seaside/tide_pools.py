from card import Card

def tide_pools_effect(player, game):
    player.draw_cards(3)
    player.actions += 1

    def next_turn(pl, g):
        n = min(2, len(pl.hand))
        to_discard = pl.choose_cards_from(pl.hand, "Tide Pools: discard 2 cards:",
                                          min_count=n, max_count=n)
        for card in to_discard:
            pl.hand.remove(card)
            pl.discard_pile.append(card)
        print(f"{pl.name} discards {n} card(s) (Tide Pools).")
    player.add_duration("Tide Pools", next_turn)

Tide_Pools = Card(
    "Tide Pools",
    cost=4,
    card_type=["Action", "Duration"],
    description="+3 Cards +1 Action. At the start of your next turn, discard 2 cards.",
    effect=tide_pools_effect,
    expansion="seaside"
)
