from behave import fixture
from unittest.mock import Mock

from scoreboard.core.app import AppModel, Application, ScoreboardView, SoundSpeaker
from scoreboard.adapters.vcs_repo_dummy import DummyVersionControlRepo

@fixture
def before_scenario(context, scenario):
    context.display = Mock(ScoreboardView)
    context.vcs = DummyVersionControlRepo()
    context.speaker = Mock(SoundSpeaker)
    context.app = Application(
        view = context.display,
        model=AppModel(),
        vcs_repo=context.vcs,
        speaker = context.speaker,
    )
    