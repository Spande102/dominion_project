from card import Card

def cutpurse_effect(player, game):
    player.coins += 2
    for other in game.attack_targets(player):
        copper = next((c for c in other.hand if c.name == "Copper"), None)
        if copper:
            other.hand.remove(copper)
            other.discard_pile.append(copper)
            print(f"{other.name} discards a Copper.")
        else:
            print(f"{other.name} reveals a hand with no Copper: {[c.name for c in other.hand]}")

Cutpurse = Card(
    "Cutpurse",
    cost=4,
    card_type=["Action", "Attack"],
    description="+2 Coins. Each other player discards a Copper (or reveals a hand with no Copper).",
    effect=cutpurse_effect,
    expansion="seaside"
)
