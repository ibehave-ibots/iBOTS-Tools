
import numpy as np
from numpy.typing import NDArray
import pytest
from hypothesis import given
from hypothesis.strategies import integers


def create_board(m, n) -> NDArray[np.bool_]:
    return np.zeros((m, n), dtype=bool)

@given(m=integers(1,1000),n=integers(1,1000))
def test_create_mxn_board(m, n):
    board = create_board(m=m, n=n)
    assert board.shape == (m, n)


def test_create_board_gives_dead_cells():
    board = create_board(m=5,n=10)
    assert np.all(board == False)

