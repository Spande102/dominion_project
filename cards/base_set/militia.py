from card import Card

def militia_effect(player, game):
    # +2 Coins
    player.coins += 2
    print(f"{player.name} gets +2 Coins.")

    for other in game.players:
        if other is not player:
            if len(other.hand) > 3:
                print(f"\n{other.name}'s hand: {[c.name for c in other.hand]}")
                while len(other.hand) > 3:
                    discard = input(f"{other.name}, choose a card to discard: ").strip()
                    card = next((c for c in other.hand if c.name.lower() == discard.lower()), None)
                    if card:
                        other.hand.remove(card)
                        other.discard_pile.append(card)
                        print(f"{other.name} discards {card.name}.")
                    else:
                        print("Invalid choice.")
            else:
                print(f"{other.name} has 3 or fewer cards, no discard needed.")

Militia = Card(
    "Militia",
    cost = 4,
    card_type = ['Action', 'Attack'],
    description = "+2 Coins. Each other player discards down to 3 cards.",
    effect = militia_effect,
    expansion = "base"
)