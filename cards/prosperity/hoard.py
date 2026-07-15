from card import Card

def hoard_effect(player, game):
    # Gold-on-Victory-buy is handled in Game.resolve_on_buy.
    return 2

Hoard = Card(
    "Hoard",
    cost=6,
    card_type=["Treasure"],
    description="+2 Coins. While this is in play, when you buy a Victory card, gain a Gold.",
    effect=hoard_effect,
    expansion="prosperity"
)
