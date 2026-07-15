from card import Card

def diplomat_effect(player, game):
    player.draw_cards(2)
    if len(player.hand) <= 5:
        player.actions += 2
        print(f"{player.name} has 5 or fewer cards in hand: +2 Actions.")

def diplomat_reaction(defender, game):
    defender.draw_cards(2)
    n = min(3, len(defender.hand))
    to_discard = defender.choose_cards_from(
        defender.hand, f"{defender.name}, discard 3 cards:", min_count=n, max_count=n)
    for card in to_discard:
        defender.hand.remove(card)
        defender.discard_pile.append(card)
    print(f"{defender.name} draws 2 and discards {n}.")
    return False  # does not block the attack

Diplomat = Card(
    "Diplomat",
    cost=4,
    card_type=["Action", "Reaction"],
    description="+2 Cards. If you have 5 or fewer cards in hand (after drawing), +2 Actions. | When another player plays an Attack, you may first reveal this from a hand of 5 or more cards, to draw 2 cards then discard 3.",
    effect=diplomat_effect,
    expansion="intrigue"
)
Diplomat.reaction_effect = diplomat_reaction
Diplomat.reaction_available = lambda defender: len(defender.hand) >= 5
