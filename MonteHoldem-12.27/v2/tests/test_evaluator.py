from pokerwin.evaluator import STRAIGHT, TWO_PAIR, HandEvaluator
from pokerwin.models import Card


def test_two_pair_kicker_with_three_pairs_uses_best_remaining_kicker() -> None:
    cards = [Card.from_string(s) for s in ["4h", "4d", "3s", "3c", "2h", "2d", "Ah"]]
    assert HandEvaluator.evaluate(cards) == (TWO_PAIR, 4, 3, 14)


def test_wheel_straight_high_card_is_five() -> None:
    cards = [Card.from_string(s) for s in ["Ah", "2d", "3s", "4c", "5h", "9d", "Kc"]]
    assert HandEvaluator.evaluate(cards) == (STRAIGHT, 5)

