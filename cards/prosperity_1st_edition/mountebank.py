from card import Card

def mountebank_effect(player, game):
    player.coins += 2
    for other in game.attack_targets(player):
        curse_in_hand = next((c for c in other.hand if c.name == "Curse"), None)
        if curse_in_hand and other.confirm(
                f"{other.name}, discard a Curse to avoid Mountebank?"):
            other.hand.remove(curse_in_hand)
            other.discard_pile.append(curse_in_hand)
            print(f"{other.name} discards a Curse and is unaffected.")
        else:
            if other.gain_card(game, game.find_supply_pile("Curse")):
                print(f"{other.name} gains a Curse.")
            if other.gain_card(game, game.find_supply_pile("Copper")):
                print(f"{other.name} gains a Copper.")

Mountebank = Card(
    "Mountebank",
    cost=5,
    card_type=["Action", "Attack"],
    description="+2 Coins. Each other player may discard a Curse. If they don't, they gain a Curse and a Copper.",
    effect=mountebank_effect,
    expansion="prosperity_1st_edition"
)
