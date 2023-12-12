from unittest.mock import Mock
from app.list_workshops_workflow import WorkshopRegistrationSummary
from web.view_model import AppState, ViewModel
from web.presenters import RegistrantPresenter, WorkshopPresenter



def test_show_sets_model_with_new_registrants():
    state = AppState(data=Mock())
    new_model = Mock(ViewModel)
    state.data.update_registrant_table.return_value = new_model
    presenter = RegistrantPresenter(state=state)
    presenter.show(registrants=[Mock(), Mock()])
    assert state.data is new_model

    

def test_show_update_sets_model_with_new_registrant():
    state = AppState(data=Mock())
    new_model = Mock(ViewModel)
    state.data.set_registration_status.return_value = new_model
    presenter = RegistrantPresenter(state=state)
    presenter.show_update(registrant=Mock())
    assert state.data is new_model

