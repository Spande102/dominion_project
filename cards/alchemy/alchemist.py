from card import Card

def alchemist_effect(player, game):
    player.draw_cards(2)
    player.actions += 1
    # Topdeck at cleanup (if a Potion is in play) is handled in
    # Player._cleanup_topdeck_offers.

Alchemist = Card(
    "Alchemist",
    cost=3,
    potion_cost=1,
    card_type=["Action"],
    description="+2 Cards +1 Action. When you discard this from play, if you have a Potion in play, you may put this onto your deck.",
    effect=alchemist_effect,
    expansion="alchemy"
)
