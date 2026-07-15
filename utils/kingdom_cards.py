import random

def choose_kingdom_cards(cards_by_expansion):
    print("\nChoose kingdom setup method:")
    print("1. Randomize 10 Kingdom cards")
    print("2. Manually select 10 cards by name")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return randomize_kingdom_cards(cards_by_expansion)
        elif choice == "2":
            return manually_choose_kingdom_cards(cards_by_expansion)
        else:
            print("Invalid input. Please enter 1 or 2.")

def randomize_kingdom_cards(cards_by_expansion):
    print("\nAvailable expansions:")
    expansions = list(cards_by_expansion.keys())
    for i, exp in enumerate(expansions, 1):
        print(f"{i}. {exp}")

    selected = input("\nEnter expansion numbers to include (comma-separated), or press Enter for all: ").strip()

    if selected:
        try:
            chosen_expansions = [expansions[int(i.strip()) - 1] for i in selected.split(",")]
        except (ValueError, IndexError):
            print("Invalid input. Using all expansions instead.")
            chosen_expansions = expansions
    else:
        chosen_expansions = expansions

    kingdom = random_kingdom(cards_by_expansion, chosen_expansions)
    if not kingdom:
        print("Not enough eligible cards available for random selection.")
    return kingdom


def random_kingdom(cards_by_expansion, expansions=None, count=10):
    """Pick a random kingdom without prompting (used by automated matches)."""
    pool = [
        card for exp in (expansions or cards_by_expansion)
        for card in cards_by_expansion[exp]
        if is_kingdom_card(card)
    ]
    if len(pool) < count:
        return []
    return random.sample(pool, count)

def manually_choose_kingdom_cards(cards_by_expansion):
    print("\nAvailable Kingdom cards:")
    all_kingdom_cards = {}

    for expansion, cards in cards_by_expansion.items():
        print(f"\n[{expansion}]")
        for card in cards:
            if is_kingdom_card(card):
                print(f" - {card.name} ({', '.join(card.card_type)})")
                all_kingdom_cards[card.name.lower()] = card

    selected_cards = []
    while len(selected_cards) < 10:
        name = input(f"\nEnter card name ({len(selected_cards) + 1}/10): ").strip().lower()
        if name in all_kingdom_cards:
            card = all_kingdom_cards[name]
            if card in selected_cards:
                print("You've already selected that card.")
            else:
                selected_cards.append(card)
        else:
            print("Card not found. Please enter the exact name shown above.")

    return selected_cards

# Helper: define what counts as a base Kingdom card
def is_kingdom_card(card):
    base_cards = {"Copper", "Silver", "Gold", "Estate", "Duchy", "Province", "Curse",
                  "Platinum", "Colony", "Potion"}
    return card.name not in base_cards