from card import Card

def familiar_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    for other in game.attack_targets(player):
        if other.gain_card(game, game.find_supply_pile("Curse")):
            print(f"{other.name} gains a Curse.")

Familiar = Card(
    "Familiar",
    cost=3,
    potion_cost=1,
    card_type=["Action", "Attack"],
    description="+1 Card +1 Action. Each other player gains a Curse.",
    effect=familiar_effect,
    expansion="alchemy"
)
