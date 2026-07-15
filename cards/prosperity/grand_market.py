from card import Card

def grand_market_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    player.buys += 1
    player.coins += 2
    # "You can't buy this if you have Copper in play" is enforced in Game.can_buy.

Grand_Market = Card(
    "Grand Market",
    cost=6,
    card_type=["Action"],
    description="+1 Card +1 Action +1 Buy +2 Coins. | You can't buy this if you have Copper in play.",
    effect=grand_market_effect,
    expansion="prosperity"
)
