from card import Card

def secret_chamber_effect(player, game):
    discards = player.choose_cards_from(
        player.hand, "Discard any number of cards (+1 Coin each):")
    for card in discards:
        player.hand.remove(card)
        player.discard_pile.append(card)
    player.coins += len(discards)
    print(f"{player.name} discards {len(discards)} card(s) for +{len(discards)} Coin.")

def secret_chamber_reaction(defender, game):
    defender.draw_cards(2)
    n = min(2, len(defender.hand))
    to_topdeck = defender.choose_cards_from(
        defender.hand, f"{defender.name}, put 2 cards on top of your deck (first = top):",
        min_count=n, max_count=n)
    for card in reversed(to_topdeck):
        defender.hand.remove(card)
        defender.topdeck(card)
    print(f"{defender.name} draws 2 and topdecks {n}.")
    return False  # does not block the attack

Secret_Chamber = Card(
    "Secret Chamber",
    cost=2,
    card_type=["Action", "Reaction"],
    description="Discard any number of cards. +1 Coin per card discarded. | When another player plays an Attack card, you may reveal this from your hand. If you do, +2 Cards, then put 2 cards from your hand on top of your deck.",
    effect=secret_chamber_effect,
    expansion="intrigue_1st_edition"
)
Secret_Chamber.reaction_effect = secret_chamber_reaction
