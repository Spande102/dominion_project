from card import Card

def transmute_effect(player, game):
    if not player.hand:
        print("No cards in hand to trash.")
        return
    card = player.choose_card_from(player.hand, "Trash a card from your hand:", optional=False)
    player.hand.remove(card)
    game.trash_pile.append(card)
    print(f"{player.name} trashes {card.name}.")
    if "Action" in card.card_type:
        if player.gain_card(game, game.find_supply_pile("Duchy")):
            print(f"{player.name} gains a Duchy.")
    if "Treasure" in card.card_type:
        if player.gain_card(game, game.find_supply_pile("Transmute")):
            print(f"{player.name} gains a Transmute.")
    if "Victory" in card.card_type:
        if player.gain_card(game, game.find_supply_pile("Gold")):
            print(f"{player.name} gains a Gold.")

Transmute = Card(
    "Transmute",
    cost=0,
    potion_cost=1,
    card_type=["Action"],
    description="Trash a card from your hand. If it is an Action card, gain a Duchy; Treasure card, gain a Transmute; Victory card, gain a Gold.",
    effect=transmute_effect,
    expansion="alchemy"
)
