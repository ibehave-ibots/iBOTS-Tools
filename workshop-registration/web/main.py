import sys
sys.path.append('..')

from unittest.mock import Mock
from app import App, RegistrantWorkflows
from web.webapp import Presenter, View


from web.create_repo import create_repo

repo = create_repo()
app = App(
    workshop_workflow=Mock(),
    registrant_workflows=RegistrantWorkflows(
        registration_repo=repo,
        presenter=Presenter(),
    )
)
view = View(app=app)
view.render()