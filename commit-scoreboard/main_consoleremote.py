import git

from scoreboard.core.app import AppModel, Application
from scoreboard.adapters.vcs_repo_git import RemoteGitVersionControlRepo
from scoreboard.adapters.views_console import ConsoleView2
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker

# Get inputs
REPO_PATH = "../../retreat-workshop-practice"
REMOTE = "origin"
TEAM_BRANCHES = ['round2', 'workshop-prep']
REFERENCE_BRANCH = 'main'


# Hook up application plugins
model = AppModel(reference_branch=REFERENCE_BRANCH)
model.add_teams(TEAM_BRANCHES, interval=1)

app = Application(
    view=ConsoleView2(),
    model=model,
    vcs_repo=RemoteGitVersionControlRepo(
        git_repository=git.Repo(path=REPO_PATH), remote=REMOTE
    ),
    speaker=SounddeviceSpeaker(blocking=False),
)

# Run main update loop
app.run_loop(interval=1.5)
