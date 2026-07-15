from card import Card

def sea_witch_effect(player, game):
    player.draw_cards(2)
    for other in game.attack_targets(player):
        if other.gain_card(game, game.find_supply_pile("Curse")):
            print(f"{other.name} gains a Curse.")

    def next_turn(pl, g):
        pl.draw_cards(2)
        n = min(2, len(pl.hand))
        to_discard = pl.choose_cards_from(pl.hand, "Sea Witch: discard 2 cards:",
                                          min_count=n, max_count=n)
        for card in to_discard:
            pl.hand.remove(card)
            pl.discard_pile.append(card)
        print(f"{pl.name} draws 2 and discards {n} (Sea Witch).")
    player.add_duration("Sea Witch", next_turn)

Sea_Witch = Card(
    "Sea Witch",
    cost=5,
    card_type=["Action", "Duration", "Attack"],
    description="+2 Cards. Each other player gains a Curse. At the start of your next turn, +2 Cards, then discard 2 cards.",
    effect=sea_witch_effect,
    expansion="seaside"
)
