import git
import streamlit as st

from scoreboard.core.app import AppModel, Application
from scoreboard.adapters.vcs_repo_git import RemoteGitVersionControlRepo
from scoreboard.adapters.views_console import ConsoleView2
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker
from scoreboard.adapters.views_streamlit import TextBarStreamlitTeamScoreComponent
from scoreboard.core.scoreboard_view import ComponentScoreboardView


# Get inputs
REPO_PATH = "../../retreat-workshop-practice"
REMOTE = "origin"
TEAM_BRANCHES = ['round2', 'workshop-prep']
REFERENCE_BRANCH = 'main'


# Hook up application plugins
if not st.session_state.get('app'):
    model = AppModel(reference_branch=REFERENCE_BRANCH)
    model.add_teams(TEAM_BRANCHES, interval=1)

    view = ComponentScoreboardView(component_factory=TextBarStreamlitTeamScoreComponent)
    view.init(model=model)

    st.session_state['app'] = Application(
        view=view,
        model=model,
        vcs_repo=RemoteGitVersionControlRepo(
            git_repository=git.Repo(path=REPO_PATH), remote=REMOTE
        ),
        speaker=SounddeviceSpeaker(blocking=False),
    )

app = st.session_state['app']
app.run_loop(interval=3)
