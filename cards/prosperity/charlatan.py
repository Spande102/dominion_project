from card import Card

def charlatan_effect(player, game):
    player.coins += 3
    for other in game.attack_targets(player):
        if other.gain_card(game, game.find_supply_pile("Curse")):
            print(f"{other.name} gains a Curse.")

Charlatan = Card(
    "Charlatan",
    cost=5,
    card_type=["Action", "Attack"],
    description="+3 Coins. Each other player gains a Curse.",
    effect=charlatan_effect,
    expansion="prosperity"
)
