from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randint
import time
from typing import Any, Type

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


class TextBarStreamlitTeamScoreComponent(TeamScoreComponent):

    def __init__(self, fontsize: str = "20px"):
        self.fontsize = fontsize
        col1, col2 = st.columns([1, 8])
        with col1:
            self.name_widget = st.empty()
        with col2:
            self.score_widget = st.empty()
    
    def render(self, name: str, score: int):
        self.name_widget.markdown(f'<p style="font-size:{self.fontsize};border-radius:2%;">{name}</p>', unsafe_allow_html=True)
        score_with_bar = "".join(["|" for _ in range(score)]) + f" {score}"
        self.score_widget.markdown(f'<p style="font-size:{self.fontsize};border-radius:2%;">{score_with_bar}</p>', unsafe_allow_html=True)


class TextScoreboardView(ScoreboardView):

    def __init__(self, component_factory: Type[TeamScoreComponent] = TextStreamlitTeamScoreComponent) -> None:
        self.team_components: dict[str, Type[TeamScoreComponent]] = None
        self.component_factory = component_factory

    def init(self, model: AppModel) -> None:
        self.team_components = {name: self.component_factory() for name in model.statuses.keys()}

    def update(self, model: AppModel) -> None:
        for team_name, widget in self.team_components.items():
            widget.render(name=team_name, score=model.statuses[team_name].points)


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
    view = TextScoreboardView(component_factory=TextBarStreamlitTeamScoreComponent)
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
    app.update_points()
    time.sleep(1)
