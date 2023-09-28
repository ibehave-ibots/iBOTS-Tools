from unittest.mock import Mock
from fern import Fern
from transformation_values import trans_list



@given(u'no points have been generated')
def step_impl(context):
    pass


@when(u'the fern is created')
def step_impl(context):
    context.fern = Fern([Mock(), Mock()])


@then(u'the first point is (0,0)')
def step_impl(context):
    assert context.fern.points == [(0,0)]


@given(u'only a first point exists')
def step_impl(context):
    context.fern = Fern(trans_list)
    assert len(context.fern.points) == 1

@when(u'the next point is calculated')
def step_impl(context):
    context.fern.calc_next_point()


@then(u'the fern consists of two points')
def step_impl(context):
    assert len(context.fern.points) ==2


@then(u'the fern consists of {n:d} calculated points')
def step_impl(context, n):
    assert len(context.fern.points) == n


@when(u'{n:d} points of the fern are calculated')
def step_impl(context, n):
    context.fern = Fern(trans_list)
    context.fern.calc_points(n)