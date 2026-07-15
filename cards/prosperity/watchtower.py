from card import Card

def watchtower_effect(player, game):
    while len(player.hand) < 6:
        card = player.draw_cards(1, return_card=True)
        if not card:
            break
        player.hand.append(card)
    # The on-gain reaction (trash or topdeck the gained card) is handled
    # in Player.gain_card.

Watchtower = Card(
    "Watchtower",
    cost=3,
    card_type=["Action", "Reaction"],
    description="Draw until you have 6 cards in hand. | When you gain a card, you may reveal this from your hand, to either trash that card or put it onto your deck.",
    effect=watchtower_effect,
    expansion="prosperity"
)
