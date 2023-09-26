from unittest.mock import Mock
from web.observable import Signal, Observable


def test_signal_doesnt_call_functions_on_connection():
    signal = Signal()
    fun1 = Mock()

    signal.connect(fun1)
    
    fun1.assert_not_called()


def test_signal_pipes_data_to_all_connected_functions():
    signal = Signal()
    fun1 = Mock()
    fun2 = Mock()

    signal.connect(fun1)
    
    signal.send(hi='hello')
    fun1.assert_called_once_with(hi='hello')
    fun2.assert_not_called()

    signal.connect(fun2)
    signal.send(bye='goodbye')
    fun1.assert_called_with(bye='goodbye')
    fun2.assert_called_once_with(bye='goodbye')

    
    

def test_state_sends_update_whenever_a_new_model_is_set():
    update_signal = Mock()
    state = Observable(data=Mock(), updated=update_signal)
    update_signal.send.assert_not_called()

    for _ in range(3):
        new_model = Mock()
        state.data = new_model
        update_signal.send.assert_called_with(new_model)


def tests_state_sendall_sends_update():
    update_signal = Mock()
    data = Mock()
    state = Observable(data=data, updated=update_signal)

    update_signal.send.assert_not_called()
    state.send_all()
    update_signal.send.assert_called_with(data)

        