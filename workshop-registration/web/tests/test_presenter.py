from unittest.mock import Mock
import pytest
from web.model import AppModel, AppState
from web.presenter import Presenter, RegistrantSummary




def test_show_sets_model_with_new_registrants():
    state = Mock(AppState)
    state.model = Mock(AppModel)
    new_model = Mock(AppModel)
    state.model.update_registrant_table.return_value = new_model
    presenter = Presenter(state=state)
    presenter.show(registrants=[Mock(), Mock()])
    assert state.model is new_model

    

def test_show_update_sets_model_with_new_registrant():
    state = Mock(AppState)
    state.model = Mock(AppModel)
    new_model = Mock(AppModel)
    state.model.set_registration_status.return_value = new_model
    presenter = Presenter(state=state)
    presenter.show_update(registrant=Mock())
    assert state.model is new_model
