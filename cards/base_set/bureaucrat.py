from card import Card

def bureaucrat_effect(player, game):
    silver = game.topdeck_gained_card(player, "Silver")
    if not silver:
        print("No Silver available in the supply!")

    for other in game.attack_targets(player):
        victory_cards = [c for c in other.hand if "Victory" in c.card_type]
        if victory_cards:
            if len(victory_cards) > 1:
                chosen = other.choose_card_from(
                    victory_cards, f"{other.name}, choose a Victory card to topdeck:", optional=False)
            else:
                chosen = victory_cards[0]
            other.hand.remove(chosen)
            other.topdeck(chosen)
            print(f"{other.name} topdecks {chosen.name}.")
        else:
            print(f"{other.name} reveals a hand with no Victory cards: {[c.name for c in other.hand]}")

Bureaucrat = Card(
    "Bureaucrat",
    cost=4,
    card_type=['Action', 'Attack'],
    description="Gain a Silver onto your deck. Each other player reveals a Victory card from their hand and puts it onto their deck (or reveals a hand with no Victory cards).",
    effect=bureaucrat_effect,
    expansion="base"
)
