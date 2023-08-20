import time
import git

from scoreboard.controllers import run_simulation
from scoreboard.core.app import AppModel, Application
from scoreboard.adapters.vcs_repo_git import RemoteGitVersionControlRepo
from scoreboard.adapters.views_console import ConsoleView2
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker


model = AppModel(reference_branch='main')
model.add_teams(['round2', 'workshop-prep'], interval=1)

vcs = RemoteGitVersionControlRepo(git.Repo('../../retreat-workshop-practice'), remote='origin')

app = Application(
    view=ConsoleView2(),
    model=model,
    vcs_repo=vcs,
    speaker=SounddeviceSpeaker(blocking=False),
)

while True:
    app.update()
    time.sleep(1.5)

