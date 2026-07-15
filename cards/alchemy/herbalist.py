from card import Card

def herbalist_effect(player, game):
    player.buys += 1
    player.coins += 1
    # Topdecking a Treasure from play at cleanup is handled in
    # Player._cleanup_topdeck_offers.

Herbalist = Card(
    "Herbalist",
    cost=2,
    card_type=["Action"],
    description="+1 Buy +1 Coin. Once this turn, when you discard a Treasure from play, you may put it onto your deck.",
    effect=herbalist_effect,
    expansion="alchemy"
)
