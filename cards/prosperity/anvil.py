from card import Card

def anvil_effect(player, game):
    treasures = [c for c in player.hand if "Treasure" in c.card_type]
    if treasures:
        to_discard = player.choose_card_from(
            treasures, "You may discard a Treasure to gain a card costing up to 4:")
        if to_discard:
            player.hand.remove(to_discard)
            player.discard_pile.append(to_discard)
            pile_name = player.choose_supply_pile(
                game, "Gain a card costing up to 4:",
                predicate=game.costs_at_most(4), optional=False)
            gained = player.gain_card(game, pile_name)
            if gained:
                print(f"{player.name} gains {gained.name}.")
    return 1  # +1 Coin

Anvil = Card(
    "Anvil",
    cost=3,
    card_type=["Treasure"],
    description="+1 Coin. You may discard a Treasure to gain a card costing up to 4.",
    effect=anvil_effect,
    expansion="prosperity"
)
