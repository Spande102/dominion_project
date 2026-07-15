from card import Card

def sailor_effect(player, game):
    player.actions += 1

    # Simplification: the official "once this turn, you may play a Duration
    # card when you gain it" clause is not implemented.
    def next_turn(pl, g):
        pl.coins += 2
        print(f"{pl.name} gets +2 Coins (Sailor).")
        if pl.hand:
            card = pl.choose_card_from(pl.hand, "Sailor: you may trash a card from your hand:",
                                       optional=True)
            if card:
                pl.hand.remove(card)
                g.trash_pile.append(card)
                print(f"{pl.name} trashes {card.name}.")
    player.add_duration("Sailor", next_turn)

Sailor = Card(
    "Sailor",
    cost=4,
    card_type=["Action", "Duration"],
    description="+1 Action. At the start of your next turn, +2 Coins and you may trash a card from your hand.",
    effect=sailor_effect,
    expansion="seaside"
)
