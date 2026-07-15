from card import Card

def vault_effect(player, game):
    player.draw_cards(2)
    discards = player.choose_cards_from(
        player.hand, "Discard any number of cards (+1 Coin each):")
    for card in discards:
        player.hand.remove(card)
        player.discard_pile.append(card)
    player.coins += len(discards)
    print(f"{player.name} discards {len(discards)} for +{len(discards)} Coins.")

    for other in game.other_players(player):
        if len(other.hand) >= 2 and other.confirm(
                f"{other.name}, discard 2 cards to draw 1?"):
            to_discard = other.choose_cards_from(
                other.hand, "Choose 2 cards to discard:", min_count=2, max_count=2)
            for card in to_discard:
                other.hand.remove(card)
                other.discard_pile.append(card)
            other.draw_cards(1)
            print(f"{other.name} discards 2 and draws 1.")

Vault = Card(
    "Vault",
    cost=5,
    card_type=["Action"],
    description="+2 Cards. Discard any number of cards for +1 Coin each. Each other player may discard 2 cards, to draw a card.",
    effect=vault_effect,
    expansion="prosperity"
)
