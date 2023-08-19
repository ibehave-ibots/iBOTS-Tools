from random import randint
import time

import streamlit as st

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, TeamSettings, TeamState
from scoreboard.core.scoreboard_view import ComponentScoreboardView

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
    for team in app.model.statuses:
        dummy_vcs_repo.branch_commits[team] += randint(0, 3)
    app.update()
    time.sleep(1)
