from random import randint
import time

import streamlit as st

from scoreboard.core.app import AppModel, Application
from scoreboard.core.scoreboard_view import ComponentScoreboardView

from scoreboard.adapters.vcs_repo_dummy import DummyVersionControlRepo
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker
from scoreboard.adapters.views_streamlit import TextBarStreamlitTeamScoreComponent


# Create View
branch_names = [f'team-{n}' for n in range(1, 4)] 

model = AppModel(reference_branch='main')
for name in branch_names:
    model.add_team(name, points=0, interval=10)
    

dummy_vcs_repo = DummyVersionControlRepo(**{'main': 0} | {name: 0 for name in branch_names})

if not st.session_state.get('app'):
    view = ComponentScoreboardView(component_factory=TextBarStreamlitTeamScoreComponent)
    view.init(model=model)
    app = Application(
        view=view,
        model=model,
        vcs_repo=dummy_vcs_repo,
        speaker=SounddeviceSpeaker(),
    )
    st.session_state['app'] = app

while True:    
    new_commits = {team: randint(0, 2) for team in app.model.team_names}
    dummy_vcs_repo.make_commits(**new_commits)
    app.update()
    time.sleep(1)
