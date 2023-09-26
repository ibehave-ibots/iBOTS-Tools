import pytest 
from fern import Transformation


def test_initiate_transformation():
    T2 = [[0.85, 0.04],
              [-0.04, 0.85]]
    offset = [1,4]
    probability = 0.5
    trans = Transformation(T2,offset, probability)

    assert trans.zero_zero == 0.85
    assert trans.zero_one == 0.04
    assert trans.one_zero == -0.04
    assert trans.one_one == 0.85

    assert trans.x_offset == 1
    assert trans.y_offset == 4

    assert trans.probability == 0.5


