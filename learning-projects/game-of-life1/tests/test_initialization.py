
import numpy as np
from numpy.typing import NDArray
import pytest
from hypothesis import given
from hypothesis.strategies import integers
from scipy.signal import convolve2d


def create_dead_board(m, n) -> NDArray[np.bool_]:
    return np.zeros((m, n), dtype=bool)

def create_random_board(m, n) -> NDArray[np.bool_]:
    return np.random.randint(0, 2, size=(m, n), dtype=bool)

@given(m=integers(1,1000),n=integers(1,1000))
def test_create_mxn_dead_board(m, n):
    board = create_dead_board(m=m, n=n)
    assert board.shape == (m, n)

def test_create_dead_board_gives_dead_cells():
    board = create_dead_board(m=5, n=10)
    assert np.all(board == False)
    
@given(m=integers(1,1000),n=integers(1,1000))
def test_create_mxn_random_board(m, n):
    board = create_random_board(m=m, n=n)
    assert board.shape == (m, n)

def test_create_random_board_gives_dead_and_alive_cells():
    board = create_random_board(m=5, n=10)
    assert not np.all(board == False)
    assert not np.all(board == True)

def count_neighbors_conv(grid):
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    return convolve2d(grid, kernel, mode='same')

def test_alive_neighbor_count():
    grid = 