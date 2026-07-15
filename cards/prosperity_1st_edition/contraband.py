from card import Card

def contraband_effect(player, game):
    player.buys += 1
    left = game.player_to_left(player)
    named = left.choose_supply_pile(
        game, f"{left.name}, name a card {player.name} can't buy this turn:", optional=False)
    if named:
        player.turn_state.forbidden_buys.add(named)
        print(f"{player.name} can't buy {named} this turn.")
    return 3

Contraband = Card(
    "Contraband",
    cost=5,
    card_type=["Treasure"],
    description="+3 Coins +1 Buy. When you play this, the player to your left names a card. You can't buy that card this turn.",
    effect=contraband_effect,
    expansion="prosperity_1st_edition"
)
