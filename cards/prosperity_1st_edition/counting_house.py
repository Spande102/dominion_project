from card import Card

def counting_house_effect(player, game):
    coppers = [c for c in player.discard_pile if c.name == "Copper"]
    if not coppers:
        print("No Coppers in your discard pile.")
        return
    options = [f"Take {n} Copper(s)" for n in range(len(coppers) + 1)]
    choice = player.choose_options(list(reversed(options)),
                                   f"Counting House ({len(coppers)} Coppers in discard):")[0]
    count = int(choice.split()[1])
    for _ in range(count):
        copper = next(c for c in player.discard_pile if c.name == "Copper")
        player.discard_pile.remove(copper)
        player.hand.append(copper)
    print(f"{player.name} puts {count} Copper(s) into hand.")

Counting_House = Card(
    "Counting House",
    cost=5,
    card_type=["Action"],
    description="Look through your discard pile, reveal any number of Copper cards from it, and put them into your hand.",
    effect=counting_house_effect,
    expansion="prosperity_1st_edition"
)
