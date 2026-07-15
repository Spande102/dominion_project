from card import Card

def mint_effect(player, game):
    treasures = [c for c in player.hand if "Treasure" in c.card_type]
    if not treasures:
        print("No Treasures in hand to reveal.")
        return
    card = player.choose_card_from(treasures, "Reveal a Treasure to gain a copy of it:")
    if card:
        gained = player.gain_card(game, game.find_supply_pile(card.name))
        if gained:
            print(f"{player.name} gains a copy of {card.name}.")
    # On buying Mint, all Treasures in play are trashed (Game.resolve_on_buy).

Mint = Card(
    "Mint",
    cost=5,
    card_type=["Action"],
    description="You may reveal a Treasure card from your hand. Gain a copy of it. | When you buy this, trash all Treasures you have in play.",
    effect=mint_effect,
    expansion="prosperity"
)
