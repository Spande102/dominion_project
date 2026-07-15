class Card:
    """
    Cards are stateless singletons: each card file creates ONE Card instance,
    and supply piles / player decks hold repeated references to it. All
    per-player and per-turn state therefore lives on Player/TurnState, never
    on the card. Revisit (instantiate copies) when adding Duration cards.
    """
    def __init__(self, name, cost, card_type, description, effect=None, expansion="base",
                 potion_cost=0):
        self.name = name
        self.cost = cost
        self.potion_cost = potion_cost  # Alchemy: Potions required to buy
        self.card_type = [card_type] if isinstance(card_type, str) else card_type
        self.description = description
        self.effect = effect
        self.expansion = expansion

    def is_type(self, type_name):
        return type_name in self.card_type

    def play(self, player, game):
        if self.effect:
            self.effect(player, game)
