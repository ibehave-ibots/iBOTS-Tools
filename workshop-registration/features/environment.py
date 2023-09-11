from unittest.mock import Mock
from behave import fixture

from app.list_workshops_app import ListWorkshopsPresenter
from app import ListWorkshopsWorkflow
from adapters import InMemoryWorkshopRepo, InMemoryRegistrationRepo

@fixture
def before_scenario(context, scenario):
    context.presenter = Mock(ListWorkshopsPresenter)
    workshop_repo = InMemoryWorkshopRepo()
    registration_repo = InMemoryRegistrationRepo()
    context.workshop_repo = workshop_repo
    context.registration_repo = registration_repo
    context.app = ListWorkshopsWorkflow(
        workshop_repo=workshop_repo, 
        registration_repo=registration_repo, 
        presenter=context.presenter,
    )
