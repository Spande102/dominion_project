from card import Card

def royal_seal_effect(player, game):
    # Topdeck-on-buy is handled in Game.resolve_on_buy
    # (simplified: buys only, not all gains).
    return 2

Royal_Seal = Card(
    "Royal Seal",
    cost=5,
    card_type=["Treasure"],
    description="+2 Coins. While this is in play, when you gain a card, you may put that card onto your deck.",
    effect=royal_seal_effect,
    expansion="prosperity_1st_edition"
)
