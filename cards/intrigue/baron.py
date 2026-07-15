from card import Card

def baron_effect(player, game):
    player.buys += 1
    estate = next((c for c in player.hand if c.name == "Estate"), None)
    if estate and player.confirm("Discard an Estate for +4 Coins?"):
        player.hand.remove(estate)
        player.discard_pile.append(estate)
        player.coins += 4
        print(f"{player.name} discards an Estate for +4 Coins.")
    else:
        gained = player.gain_card(game, game.find_supply_pile("Estate"))
        if gained:
            print(f"{player.name} gains an Estate.")
        else:
            print("No Estates left to gain.")

Baron = Card(
    "Baron",
    cost=4,
    card_type=["Action"],
    description="+1 Buy. You may discard an Estate for +4 Coins. If you don't, gain an Estate.",
    effect=baron_effect,
    expansion="intrigue"
)
