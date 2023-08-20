import git
import streamlit as st

from scoreboard.core.app import AppModel, Application
from scoreboard.adapters.vcs_repo_git import RemoteGitVersionControlRepo
from scoreboard.adapters.views_console import ConsoleView2
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker
from scoreboard.adapters.views_streamlit import TextBarStreamlitTeamScoreComponent, BarPlotStreamlitTeamScoreComponent
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

    st.title('Workshop: Scripting Collaborative Stories with Data Pipelines')
    "---"
    view = ComponentScoreboardView(component_factory=BarPlotStreamlitTeamScoreComponent)
    view.init(model=model)
    "---"
    st.write('Book a session with us: link to website')
    st.write('Sign up for "Intro to Python Workshop" on date1:')
    st.write('Sign up for "Intro to Python Workshop" on date2:')

    st.session_state['app'] = Application(
        view=view,
        model=model,
        vcs_repo=RemoteGitVersionControlRepo(git_repository=git.Repo(path=REPO_PATH), remote=REMOTE),
        speaker=SounddeviceSpeaker(blocking=False),
    )

app = st.session_state['app']
app.run_loop(interval=3)
