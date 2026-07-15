from card import Card

def trade_route_effect(player, game):
    player.buys += 1
    if player.hand:
        card = player.choose_card_from(player.hand, "Trash a card from your hand:", optional=False)
        player.hand.remove(card)
        game.trash_pile.append(card)
        print(f"{player.name} trashes {card.name}.")
    value = len(game.trade_route_gained)
    player.coins += value
    print(f"Trade Route: +{value} Coins ({value} Victory pile(s) gained from).")

Trade_Route = Card(
    "Trade Route",
    cost=3,
    card_type=["Action"],
    description="+1 Buy. Trash a card from your hand. +1 Coin per Victory card pile that has had a card gained from it this game.",
    effect=trade_route_effect,
    expansion="prosperity_1st_edition"
)
