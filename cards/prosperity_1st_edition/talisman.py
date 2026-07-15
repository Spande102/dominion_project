from card import Card

def talisman_effect(player, game):
    # Copy-on-buy is handled in Game.resolve_on_buy.
    return 1

Talisman = Card(
    "Talisman",
    cost=4,
    card_type=["Treasure"],
    description="+1 Coin. While this is in play, when you buy a non-Victory card costing 4 or less, gain a copy of it.",
    effect=talisman_effect,
    expansion="prosperity_1st_edition"
)
