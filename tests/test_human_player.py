"""Tests for HumanPlayer's terminal prompts, driven by monkeypatched input."""
from human_player import HumanPlayer
from cards.base_set.copper import Copper
from cards.base_set.estate import Estate


def feed(monkeypatch, answers):
    answers = list(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": answers.pop(0))


def test_choose_options_single(monkeypatch):
    p = HumanPlayer("H")
    feed(monkeypatch, ["9", "2"])   # invalid, then option 2
    assert p.choose_options(["+2 Cards", "+2 Coins"], "Choose:") == ["+2 Coins"]


def test_choose_options_multiple_distinct(monkeypatch):
    p = HumanPlayer("H")
    feed(monkeypatch, ["1,1", "1,3"])   # duplicate rejected, then valid
    assert p.choose_options(["a", "b", "c"], "Choose:", count=2) == ["a", "c"]


def test_choose_cards_from_enforces_count(monkeypatch):
    p = HumanPlayer("H")
    p.hand = [Copper, Estate, Copper]
    feed(monkeypatch, ["1", "1,2"])   # too few, then exactly two
    chosen = p.choose_cards_from(p.hand, "Discard:", min_count=2, max_count=2)
    assert chosen == [Copper, Estate]


def test_confirm(monkeypatch):
    p = HumanPlayer("H")
    feed(monkeypatch, ["maybe", "y"])
    assert p.confirm("Sure?") is True
    feed(monkeypatch, ["n"])
    assert p.confirm("Sure?") is False
