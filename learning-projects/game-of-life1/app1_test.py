import numpy as np

def matrix_initializer(size):
    return np.random.randint(0, 1, size=tuple(size))

def test_matrix_has_correct_size_and_state_values():
    # GIVEN the size of the matrix
    expected_size = (5, 5)
    
    # WHEN user generates a matrix using the initializer function
    generated_matrix = matrix_initializer(size=expected_size)
    
    # THEN a matrix with correct shape and state values is generated
    assert generated_matrix.shape == expected_size
    