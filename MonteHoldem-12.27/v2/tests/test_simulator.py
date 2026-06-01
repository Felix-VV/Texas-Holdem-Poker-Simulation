import pytest

from pokerwin.models import Card
from pokerwin.simulator import calculate_equity_percent


def test_tie_splitting_equity_when_board_is_royal_flush() -> None:
    hero = [Card.from_string("2c"), Card.from_string("3d")]
    board = [Card.from_string(s) for s in ["Ah", "Kh", "Qh", "Jh", "Th"]]

    equity = calculate_equity_percent(hero, board=board, players=4, sims=50, seed=123)

    assert equity == pytest.approx(25.0)

