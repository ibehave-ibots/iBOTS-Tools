from unittest.mock import Mock
from web.signal import Signal


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

    
    
    


