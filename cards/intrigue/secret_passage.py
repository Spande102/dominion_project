from card import Card

def secret_passage_effect(player, game):
    player.draw_cards(2)
    player.actions += 1
    if not player.hand:
        return
    card = player.choose_card_from(
        player.hand, "Take a card from your hand to put into your deck:", optional=False)
    player.hand.remove(card)
    # Simplified: top or bottom of the deck (official allows any position)
    if player.confirm(f"Put {card.name} on TOP of your deck? (otherwise the bottom)"):
        player.topdeck(card)
    else:
        player.deck.insert(0, card)
    print(f"{player.name} tucks a card into their deck.")

Secret_Passage = Card(
    "Secret Passage",
    cost=4,
    card_type=["Action"],
    description="+2 Cards +1 Action. Take a card from your hand and put it anywhere in your deck.",
    effect=secret_passage_effect,
    expansion="intrigue"
)
