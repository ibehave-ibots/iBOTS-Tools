from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randint
import time
from typing import Any

import streamlit as st

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, TeamSettings, ScoreboardView, TeamState, SoundSpeaker

from scoreboard.adapters.view_console_with_sound import ConsoleWithSoundView
from scoreboard.adapters.speaker_sounddevice import SounddeviceSpeaker

# Create View

class TeamScoreComponent(ABC):

    @abstractmethod
    def render(self, name: str, score: int) -> None: ...



class TextStreamlitTeamScoreComponent(TeamScoreComponent):

    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.name_widget = st.empty()
        with col2:
            self.score_widget = st.empty()
    
    def render(self, name: str, score: int):
        self.name_widget.text(name)
        self.score_widget.text(score)


class TextScoreboardView(ScoreboardView):

    def __init__(self) -> None:
        self.team_components: dict[str, TextStreamlitTeamScoreComponent] = None

    def init(self, model: AppModel) -> None:
        self.team_components = {name: TextStreamlitTeamScoreComponent() for name in model.statuses.keys()}

    def update(self, model: AppModel) -> None:
        for team_name, widget in self.team_components.items():
            widget.render(name=team_name, score=model.statuses[team_name].points)

        

view = TextScoreboardView()
model=AppModel(
    settings={
        'team-1': TeamSettings(interval=6),
        'team-2': TeamSettings(interval=6),
        'team-3': TeamSettings(interval=4),
        'team-4': TeamSettings(interval=40),
    },
    statuses={
        'team-1': TeamState(points=0),
        'team-2': TeamState(points=5),
        'team-3': TeamState(points=0),
        'team-4': TeamState(points=22),
    },
    reference_branch='main',
)
view.init(model=model)
view.update(model=model)



# # Define Layout
# team1_score = st.empty()
# team3_score = st.empty()
# team2_score = st.empty()

# team3_score.text("team 3 score")


# if not st.session_state.get('app'):
#     view = StreamlitScoreboardView(
#         scores={
#             'team-1': team1_score,
#             'team-2': team2_score,
#             'team-3': team3_score,
#         }
#     )
#     app = Application(
#         view=view,
#         model=AppModel(
#             settings={
#                 'team-1': TeamSettings(interval=6),
#                 'team-2': TeamSettings(interval=6),
#                 'team-3': TeamSettings(interval=4),
#             },
#             statuses={
#                 'team-1': TeamState(points=0),
#                 'team-2': TeamState(points=0),
#                 'team-3': TeamState(points=0),
#             },
#             reference_branch='main',
#         ),
#         vcs_repo=DummyVersionControlRepo(**{'main': 0, 'team-1': 0, 'team-2': 0, 'team-3': 0}),
#         speaker=SounddeviceSpeaker(),
#     )
#     st.session_state['app'] = app



# while True:    
#     for team in app.model.statuses:
#         app.vcs_repo.branch_commits[team] += randint(0, 2)
#     app.update_points()
#     time.sleep(1)


