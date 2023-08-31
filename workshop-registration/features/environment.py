from behave import fixture
from app import AppModel, App
from external import InMemoryWorkshopRepo, InMemoryRegistrationRepo

@fixture
def before_scenario(context, scenario):
    workshop_repo = InMemoryWorkshopRepo()
    registration_repo = InMemoryRegistrationRepo()
    app_model = AppModel()
    context.workshop_repo = workshop_repo
    context.registration_repo = registration_repo
    context.app = App(workshop_repo=workshop_repo, registration_repo=registration_repo, model=app_model)
