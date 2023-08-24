from behave import given, when, then

def add(a, b): return a + b
def sub(a, b): return a - b


@given(u'I have the number {value:d}')
def step_impl(context, value):
    context.first = value
    

@given(u'I also have the number {value:d}')
def step_impl(context, value):
    context.second = value


@when(u'I use the {operator} operator on them')
def step_impl(context, operator):
    ops = {'addition': add, 'subtraction': sub}
    op = ops[operator]
    context.result = op(a=context.first, b=context.second)


@then(u'I see the result is {value:d}')
def step_impl(context, value):
    assert context.result == value
    
    
