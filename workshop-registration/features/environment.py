from unittest.mock import Mock
from behave import fixture

from app import App, ListWorkshopsPresenter, ListWorkshopsWorkflow, ListRegistrantsWorkflow
from adapters import InMemoryWorkshopRepo, InMemoryRegistrationRepo

from app.list_registrant_presenter import ListRegistrantPresenter, RegistrantSummary

@fixture
def before_scenario(context, scenario):
    context.presenter = Mock(ListWorkshopsPresenter)
    context.workshop_repo = InMemoryWorkshopRepo()
    context.registration_repo = InMemoryRegistrationRepo()
    context.list_registrants_presenter = Mock(ListRegistrantPresenter)
    context.app = App(
        workshop_workflow = ListWorkshopsWorkflow(
            workshop_repo=context.workshop_repo, 
            registration_repo=context.registration_repo, 
            presenter=context.presenter,
        ),
        registrants_workflow=ListRegistrantsWorkflow(
                registration_repo=context.registration_repo,
                presenter=context.list_registrants_presenter,
        )
    )
