from scoreboard.controllers import run_simulation
from scoreboard.core.app import AppModel, Application
from scoreboard.adapters.vcs_repo_dummy import DummyVersionControlRepo
from scoreboard.adapters.views_console import ConsoleView2
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker


branches = ['team-1', 'team-2', 'team-3', 'team-4']

model = AppModel(reference_branch='main')
model.add_teams(branches, interval=6, points=0)

app = Application(
    view=ConsoleView2(),
    model=model,
    vcs_repo=DummyVersionControlRepo(**{'main': 0} | {name: 0 for name in branches}),
    speaker=SounddeviceSpeaker(),
)

run_simulation(app=app, vcs=app.vcs_repo)

