from behave import fixture
from unittest.mock import Mock

from scoreboard.vcs_repos import DummyVersionControlRepo
from scoreboard.app import TeamSettings, AppModel, Application, TeamState, ScoreboardView

@fixture
def before_scenario(context, scenario):
    context.display = Mock(ScoreboardView)
    context.vcs = DummyVersionControlRepo()
    context.app = Application(
        view = context.display,
        model=AppModel(),
        vcs_repo=context.vcs,
    )
    