from card import Card

def wishing_well_effect(player, game):
    player.draw_cards(1)
    player.actions += 1

    pile_name = player.choose_supply_pile(
        game, "Wishing Well - name a card:", optional=True)
    if not pile_name:
        return
    top = player.draw_cards(1, return_card=True)
    if not top:
        print("No cards left to reveal.")
        return
    print(f"{player.name} wished for {pile_name} and reveals {top.name}.")
    if top.name == pile_name:
        player.hand.append(top)
        print("The wish comes true! The card goes to hand.")
    else:
        player.topdeck(top)

Wishing_Well = Card(
    "Wishing Well",
    cost=3,
    card_type=["Action"],
    description="+1 Card +1 Action. Name a card, then reveal the top card of your deck. If you named it, put it into your hand.",
    effect=wishing_well_effect,
    expansion="intrigue"
)
