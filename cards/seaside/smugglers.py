from card import Card

def smugglers_effect(player, game):
    right = game.player_to_right(player)
    candidates = []
    seen = set()
    for card in right.gained_last_turn:
        if (card.name not in seen and game.card_cost(card) <= 6
                and card.potion_cost == 0 and game.supply.get(card.name)):
            candidates.append(card)
            seen.add(card.name)
    if not candidates:
        print(f"{right.name} gained nothing smuggleable last turn.")
        return
    chosen = player.choose_card_from(
        candidates, f"Gain a copy of a card {right.name} gained last turn:", optional=False)
    gained = player.gain_card(game, game.find_supply_pile(chosen.name))
    if gained:
        print(f"{player.name} smuggles a {gained.name}.")

Smugglers = Card(
    "Smugglers",
    cost=3,
    card_type=["Action"],
    description="Gain a copy of a card costing up to 6 that the player to your right gained on their last turn.",
    effect=smugglers_effect,
    expansion="seaside"
)
