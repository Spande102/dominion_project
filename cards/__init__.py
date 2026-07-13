import os
import importlib

from card import Card


def load_cards():
    base_path = os.path.dirname(__file__)
    all_cards = []
    cards_by_expansion = {}
    seen_names = set()

    for expansion in sorted(os.listdir(base_path)):
        exp_path = os.path.join(base_path, expansion)
        if os.path.isdir(exp_path) and not expansion.startswith('__'):
            cards_by_expansion[expansion] = []
            for card_file in sorted(os.listdir(exp_path)):
                if card_file.endswith('.py') and card_file != '__init__.py':
                    module_name = f"cards.{expansion}.{card_file[:-3]}"
                    module = importlib.import_module(module_name)
                    for attr in dir(module):
                        card = getattr(module, attr)
                        if isinstance(card, Card) and card.name not in seen_names:
                            seen_names.add(card.name)
                            all_cards.append(card)
                            cards_by_expansion[expansion].append(card)

    return all_cards, cards_by_expansion
