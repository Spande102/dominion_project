from card import Card

def peddler_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    player.coins += 1
    # Costs 2 less per Action in play (handled in Game.card_cost).

Peddler = Card(
    "Peddler",
    cost=8,
    card_type=["Action"],
    description="+1 Card +1 Action +1 Coin. | During your turn, this costs 2 Coins less per Action card you have in play.",
    effect=peddler_effect,
    expansion="prosperity"
)
