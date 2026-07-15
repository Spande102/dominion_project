from card import Card

def courtyard_effect(player, game):
    player.draw_cards(3)
    if player.hand:
        card = player.choose_card_from(
            player.hand, "Put a card from your hand onto your deck:", optional=False)
        player.hand.remove(card)
        player.topdeck(card)
        print(f"{player.name} puts a card on top of their deck.")

Courtyard = Card(
    "Courtyard",
    cost=2,
    card_type=["Action"],
    description="+3 Cards. Put a card from your hand onto your deck.",
    effect=courtyard_effect,
    expansion="intrigue"
)
