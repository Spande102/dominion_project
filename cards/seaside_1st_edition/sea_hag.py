from card import Card

def sea_hag_effect(player, game):
    for other in game.attack_targets(player):
        top = other.draw_cards(1, return_card=True)
        if top:
            other.discard_pile.append(top)
            print(f"{other.name} discards {top.name} from the top of their deck.")
        if other.gain_card(game, game.find_supply_pile("Curse"), destination='deck'):
            print(f"{other.name} gains a Curse onto their deck.")

Sea_Hag = Card(
    "Sea Hag",
    cost=4,
    card_type=["Action", "Attack"],
    description="Each other player discards the top card of their deck, then gains a Curse onto their deck.",
    effect=sea_hag_effect,
    expansion="seaside_1st_edition"
)
