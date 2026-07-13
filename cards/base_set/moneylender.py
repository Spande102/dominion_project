from card import Card

def moneylender_effect(player, game):
    copper_in_hand = next((card for card in player.hand if card.name == "Copper"), None)
    if not copper_in_hand:
        print("No Copper in hand to trash.")
        return

    if player.confirm("Trash a Copper for +3 Coins?"):
        player.hand.remove(copper_in_hand)
        game.trash_pile.append(copper_in_hand)
        player.coins += 3
        print(f"{player.name} trashes a Copper and gains +3 Coins.")
    else:
        print("No Copper trashed.")

Moneylender = Card(
    "Moneylender",
    cost=4,
    card_type=["Action"],
    description="You may trash a Copper from your hand. If you do, +3 Coins.",
    effect=moneylender_effect,
    expansion="base"
)
