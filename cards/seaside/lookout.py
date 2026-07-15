from card import Card

def lookout_effect(player, game):
    player.actions += 1
    top = player.draw_cards(3, return_card=True)
    if not top:
        print("No cards to look at.")
        return
    print(f"You look at: {[c.name for c in top]}")

    to_trash = player.choose_card_from(top, "Choose one to TRASH:", optional=False)
    top.remove(to_trash)
    game.trash_pile.append(to_trash)
    print(f"{player.name} trashes {to_trash.name}.")

    if top:
        to_discard = player.choose_card_from(top, "Choose one to DISCARD:", optional=False)
        top.remove(to_discard)
        player.discard_pile.append(to_discard)
        print(f"{player.name} discards {to_discard.name}.")

    if top:
        player.topdeck(top[0])

Lookout = Card(
    "Lookout",
    cost=3,
    card_type=["Action"],
    description="+1 Action. Look at the top 3 cards of your deck. Trash one of them. Discard one of them. Put the other one back on top of your deck.",
    effect=lookout_effect,
    expansion="seaside"
)
