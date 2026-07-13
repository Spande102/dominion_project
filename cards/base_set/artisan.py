from card import Card

def artisan_effect(player, game):
    # Gain a card to hand
    max_cost = 5
    pile_name = player.choose_supply_pile(
        game, f"Gain a card to your hand costing up to {max_cost}:",
        predicate=lambda c: c.cost <= max_cost, optional=False)
    gained_card = player.gain_card(game, pile_name, destination='hand')
    if gained_card:
        print(f"{player.name} gains {gained_card.name} to their hand.")
    else:
        print("No cards available to gain.")

    # Topdeck a card from hand
    if player.hand:
        card_to_topdeck = player.choose_card_from(
            player.hand, "Choose a card from your hand to put onto your deck:", optional=False)
        player.hand.remove(card_to_topdeck)
        player.topdeck(card_to_topdeck)
        print(f"{player.name} topdecks {card_to_topdeck.name}.")

Artisan = Card(
    "Artisan",
    cost=6,
    card_type=["Action"],
    description="Gain a card to your hand costing up to 5. Put a card from your hand onto your deck.",
    effect=artisan_effect,
    expansion="base"
)
