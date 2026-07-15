from card import Card

def treasury_effect(player, game):
    player.draw_cards(1)
    player.actions += 1
    player.coins += 1
    # The topdeck-at-cleanup option (if no Victory card was bought) is
    # handled in Player._cleanup_topdeck_offers.

Treasury = Card(
    "Treasury",
    cost=5,
    card_type=["Action"],
    description="+1 Card +1 Action +1 Coin. At the end of your Buy phase this turn, if you didn't gain a Victory card in it, you may put this onto your deck.",
    effect=treasury_effect,
    expansion="seaside"
)
