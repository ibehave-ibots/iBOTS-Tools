from random import randint
import time

import streamlit as st

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, TeamSettings, TeamState
from scoreboard.core.scoreboard_view import ComponentScoreboardView

from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker
from scoreboard.adapters.views_streamlit import TextBarStreamlitTeamScoreComponent


# Create View

model=AppModel(
    settings={
        'team-1': TeamSettings(interval=6),
        'team-2': TeamSettings(interval=6),
        'team-3': TeamSettings(interval=4),
        'team-4': TeamSettings(interval=40),
    },
    statuses={
        'team-1': TeamState(points=30),
        'team-2': TeamState(points=5),
        'team-3': TeamState(points=0),
        'team-4': TeamState(points=22),
    },
    reference_branch='main',
)

if not st.session_state.get('app'):
    view = ComponentScoreboardView(component_factory=TextBarStreamlitTeamScoreComponent)
    view.init(model=model)
    app = Application(
        view=view,
        model=model,
        vcs_repo=DummyVersionControlRepo(**{'main': 0, 'team-1': 0, 'team-2': 0, 'team-3': 0, 'team-4': 0}),
        speaker=SounddeviceSpeaker(),
    )
    st.session_state['app'] = app

while True:    
    for team in app.model.statuses:
        app.vcs_repo.branch_commits[team] += randint(0, 2)
    app.update()
    time.sleep(1)
