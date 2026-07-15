from card import Card

def pearl_diver_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    if not player.deck and player.discard_pile:
        import random
        player.deck = player.discard_pile
        player.discard_pile = []
        random.shuffle(player.deck)
    if not player.deck:
        return
    bottom = player.deck[0]
    print(f"Bottom of your deck: {bottom.name}")
    if player.confirm(f"Put {bottom.name} on top of your deck?"):
        player.deck.pop(0)
        player.topdeck(bottom)

Pearl_Diver = Card(
    "Pearl Diver",
    cost=2,
    card_type=["Action"],
    description="+1 Card +1 Action. Look at the bottom card of your deck. You may put it on top.",
    effect=pearl_diver_effect,
    expansion="seaside_1st_edition"
)
