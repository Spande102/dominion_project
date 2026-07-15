from card import Card

def sea_chart_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    top = player.draw_cards(1, return_card=True)
    if not top:
        return
    in_play_names = {c.name for c in player.in_play + player.duration_in_play}
    print(f"{player.name} reveals {top.name}.")
    if top.name in in_play_names:
        player.hand.append(top)
        print("A copy is in play - it goes to hand.")
    else:
        player.topdeck(top)

Sea_Chart = Card(
    "Sea Chart",
    cost=3,
    card_type=["Action"],
    description="+1 Card +1 Action. Reveal the top card of your deck. If you have a copy of it in play, put it into your hand.",
    effect=sea_chart_effect,
    expansion="seaside"
)
