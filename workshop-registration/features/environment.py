from behave import fixture
from registration import WorkshopRepo, AppModel, App

@fixture
def before_scenario(context, scenario):
    workshop_repo = WorkshopRepo()
    app_model = AppModel()
    context.workshop_repo = workshop_repo
    context.app = App(workshop_repo=workshop_repo, model=app_model)
