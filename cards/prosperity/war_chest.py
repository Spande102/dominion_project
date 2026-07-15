from card import Card

def war_chest_effect(player, game):
    left = game.player_to_left(player)
    named = left.choose_supply_pile(
        game, f"{left.name}, name a card (it can't be War Chest-gained this turn):",
        optional=False)
    if named:
        player.turn_state.war_chest_named.add(named)
        print(f"{left.name} names {named}.")

    banned = player.turn_state.war_chest_named
    pile_name = player.choose_supply_pile(
        game, "Gain a card costing up to 5:",
        predicate=lambda c: game.card_cost(c) <= 5 and c.potion_cost == 0
        and c.name not in banned,
        optional=False)
    gained = player.gain_card(game, pile_name)
    if gained:
        print(f"{player.name} gains {gained.name}.")
    return 0

War_Chest = Card(
    "War Chest",
    cost=5,
    card_type=["Treasure"],
    description="The player to your left names a card. Gain a card costing up to 5 that hasn't been named for War Chests this turn.",
    effect=war_chest_effect,
    expansion="prosperity"
)
