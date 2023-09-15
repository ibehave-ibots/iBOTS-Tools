import numpy as np
from numpy.typing import NDArray
from scipy.signal import convolve2d

def create_dead_board(m, n) -> NDArray[np.bool_]:
    return np.zeros((m, n), dtype=bool)

def create_random_board(m, n) -> NDArray[np.bool_]:
    return np.random.randint(0, 2, size=(m, n), dtype=bool)

def count_alive_neighbors(grid):
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])
    return convolve2d(grid, kernel, mode='same')

def update_board_state(current_state):
    new_state = np.zeros_like(current_state)
    alive_neighbors_count = count_alive_neighbors(current_state)
    # dead to alive or stay alive
    new_state[alive_neighbors_count == 3] = 1
    # stay alive
    new_state[(current_state == 1) & (alive_neighbors_count == 2)] = 1
    return new_state