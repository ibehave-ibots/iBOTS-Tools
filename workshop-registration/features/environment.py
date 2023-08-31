from behave import fixture
from registration import WorkshopRepo, RegistrationRepo, AppModel, App

@fixture
def before_scenario(context, scenario):
    workshop_repo = WorkshopRepo()
    registration_repo = RegistrationRepo()
    app_model = AppModel()
    context.workshop_repo = workshop_repo
    context.registration_repo = registration_repo
    context.app = App(workshop_repo=workshop_repo, registration_repo=registration_repo, model=app_model)
