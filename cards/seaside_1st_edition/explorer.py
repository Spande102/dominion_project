from card import Card

def explorer_effect(player, game):
    province = next((c for c in player.hand if c.name == "Province"), None)
    if province and player.confirm("Reveal a Province from your hand?"):
        if player.gain_card(game, game.find_supply_pile("Gold"), destination='hand'):
            print(f"{player.name} gains a Gold to their hand.")
    else:
        if player.gain_card(game, game.find_supply_pile("Silver"), destination='hand'):
            print(f"{player.name} gains a Silver to their hand.")

Explorer = Card(
    "Explorer",
    cost=5,
    card_type=["Action"],
    description="You may reveal a Province from your hand. If you do, gain a Gold to your hand; if you don't, gain a Silver to your hand.",
    effect=explorer_effect,
    expansion="seaside_1st_edition"
)
