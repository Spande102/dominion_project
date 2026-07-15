from card import Card

def torturer_effect(player, game):
    player.draw_cards(3)
    for other in game.attack_targets(player):
        choice = other.choose_options(
            ["Discard 2 cards", "Gain a Curse to your hand"],
            f"{other.name} - Torturer, choose one:")[0]
        if choice == "Discard 2 cards":
            n = min(2, len(other.hand))
            to_discard = other.choose_cards_from(
                other.hand, f"{other.name}, choose 2 cards to discard:",
                min_count=n, max_count=n)
            for card in to_discard:
                other.hand.remove(card)
                other.discard_pile.append(card)
                print(f"{other.name} discards {card.name}.")
        else:
            curse = other.gain_card(game, game.find_supply_pile("Curse"), destination='hand')
            if curse:
                print(f"{other.name} gains a Curse to their hand.")
            else:
                print("No Curses left to gain.")

Torturer = Card(
    "Torturer",
    cost=5,
    card_type=["Action", "Attack"],
    description="+3 Cards. Each other player either discards 2 cards or gains a Curse to their hand, their choice.",
    effect=torturer_effect,
    expansion="intrigue"
)
