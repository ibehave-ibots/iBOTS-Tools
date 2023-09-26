import os
from unittest.mock import Mock
from fern import Fern, Transformation
import pytest
import numpy as np
from transformation_values import trans_list

def test_first_point():
    T1 = Mock()
    T2 = Mock()
    fern = Fern([T1,T2])
    assert fern.points[0] == (0,0)

@pytest.mark.parametrize('p', [0.2, 0.5, 0.9])
def test_get_next_transform_probability_choice(p):
    
    tol = 0.02
    n = 10000

    T1 = Mock(probability = p, id_tag=1)
    T2 = Mock(probability = 1-p, id_tag=2)
    fern = Fern([T1,T2])
    
    transforms = [fern.get_next_transform() for _ in range(0,n)]
    num_T1s = len(list(filter(lambda x: x.id_tag==1, transforms)))
    assert num_T1s > (p-tol)*n and num_T1s < (p+tol)*n

def test_apply_transformation():
    fern = Fern([])
    trans = Transformation(matrix =[[1, 2], [3, 4]] , offset= [99, 1.6],probability=Mock())

    new_point=fern.apply_transformation(trans, (1.5,1.0))

    assert new_point == (102.5, 10.1)


def test_calc_next_point():
    fern = Fern([Transformation([[5, 1], [0, 4]], [1, 0], 1.0)])
    fern.calc_next_point()

    assert len(fern.points) ==2
    assert fern.points[-1] == (1, 0)

def test_calc_many_points():
    fern = Fern([Transformation([[1, 0], [0, 1]], [1, 1], 1.0)])
    fern.calc_points(n=10)

    assert len(fern.points)==10
    assert fern.points[3] == (3, 3)


def test_save_points(delete_output_file = True):

    fern = Fern([Mock(),Mock()])
    initial_point = (np.random.randint(1000), np.random.randint(1000))
    second_point = (np.random.randint(1000), np.random.randint(1000))
    fern.points =[initial_point, second_point]
    fern.save_points('test.dat')

    assert os.path.isfile('test.dat')

    with open('test.dat', 'r') as f:
        lines = f.readlines()

    assert lines[1] == '%.5f, %.5f\n' %(initial_point[0], initial_point[1])
    assert lines[2] == '%.5f, %.5f\n' %(second_point[0], second_point[1])

    if delete_output_file: os.remove('test.dat')






