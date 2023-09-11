from unittest.mock import Mock
from behave import fixture

from app import App, ListWorkshopsPresenter, ListWorkshopsWorkflow
from adapters import InMemoryWorkshopRepo, InMemoryRegistrationRepo

@fixture
def before_scenario(context, scenario):
    context.presenter = Mock(ListWorkshopsPresenter)
    context.workshop_repo = InMemoryWorkshopRepo()
    context.registration_repo = InMemoryRegistrationRepo()
    context.app = App(
        workshop_workflow = ListWorkshopsWorkflow(
            workshop_repo=context.workshop_repo, 
            registration_repo=context.registration_repo, 
            presenter=context.presenter,
        ),
        registrants_workflow=Mock()
    )
