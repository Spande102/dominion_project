from card import Card

def vassal_effect(player, game):
    player.coins += 2
    top = player.draw_cards(1, return_card=True)
    if top:
        print(f"Discarded {top.name}.")
        player.discard_pile.append(top)
        if "Action" in top.card_type:
            if player.confirm(f"Play {top.name}?"):
                player.discard_pile.remove(top)
                player.in_play.append(top)
                if top.effect:
                    top.effect(player, game)

Vassal = Card(
    "Vassal",
    cost=4,
    card_type=["Action"],
    description="+2 Coins. Discard the top card of your deck. If it's an Action card, you may play it.",
    effect=vassal_effect,
    expansion="base",
)
