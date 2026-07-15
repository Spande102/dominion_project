from card import Card

def collection_effect(player, game):
    player.buys += 1
    # +1 VP per Action gained while in play: handled in Game.notify_gain.
    return 2

Collection = Card(
    "Collection",
    cost=5,
    card_type=["Treasure"],
    description="+2 Coins +1 Buy. While this is in play, when you gain an Action card, +1 VP.",
    effect=collection_effect,
    expansion="prosperity"
)
