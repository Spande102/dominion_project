from card import Card

def city_effect(player, game):
    empty = sum(1 for pile in game.supply.values() if not pile)
    player.draw_cards(1)
    player.actions += 2
    if empty >= 1:
        player.draw_cards(1)
    if empty >= 2:
        player.coins += 1
        player.buys += 1
    if empty:
        print(f"City boosted by {empty} empty pile(s).")

City = Card(
    "City",
    cost=5,
    card_type=["Action"],
    description="+1 Card +2 Actions. If there are one or more empty Supply piles, +1 Card. If there are two or more, +1 Coin and +1 Buy.",
    effect=city_effect,
    expansion="prosperity"
)
