
import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import integers
import numpy.testing as npt
from app import (
    create_dead_board, 
    create_random_board, 
    count_alive_neighbors, 
    update_board_state)

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

def test_alive_neighbors_count():
    board = np.array([[1, 0, 0], 
                     [1, 0, 1], 
                     [0, 1, 0]])
    
    alive_neighbors_count = count_alive_neighbors(board)
    
    expected_alive_neighbors_count = np.array([[1, 3, 1], 
                                               [2, 4, 1], 
                                               [2, 2, 2]])
    npt.assert_equal(alive_neighbors_count, expected_alive_neighbors_count)

def test_state_update_from_dead_to_alive():
    board_state1 = np.array([[1, 0, 0, 1], 
                             [1, 0, 1, 1], 
                             [0, 1, 0, 0],
                             [0, 0, 0, 0]])
    
    expected_baord_state2 = np.array([[0, 1, 1, 1], 
                                      [1, 0, 1, 1], 
                                      [0, 1, 1, 0],
                                      [0, 0, 0, 0]])
    
    baord_state2 = update_board_state(board_state1)
    
    npt.assert_equal(baord_state2, expected_baord_state2)