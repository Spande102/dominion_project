from card import Card

def navigator_effect(player, game):
    player.coins += 2
    top = player.draw_cards(5, return_card=True)
    if not top:
        return
    print(f"You look at: {[c.name for c in top]}")
    choice = player.choose_options(
        ["Put them back in any order", "Discard them all"], "Navigator:")[0]
    if choice.startswith("Discard"):
        player.discard_pile.extend(top)
        print(f"{player.name} discards all 5.")
    else:
        ordered = player.order_cards(top, "Put back on your deck (first = top):")
        for card in reversed(ordered):
            player.topdeck(card)

Navigator = Card(
    "Navigator",
    cost=4,
    card_type=["Action"],
    description="+2 Coins. Look at the top 5 cards of your deck. Either discard them all, or put them back in any order.",
    effect=navigator_effect,
    expansion="seaside_1st_edition"
)
