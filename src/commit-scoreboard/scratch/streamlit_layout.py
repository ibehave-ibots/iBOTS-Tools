from abc import ABC, abstractmethod
import streamlit as st


class TeamScoreComponent(ABC):

    @abstractmethod
    def render(self, name: str, score: int) -> None: ...



class TextTeamScoreComponent(TeamScoreComponent):

    def __init__(self):
        col1, col2 = st.columns(2)
        with col1:
            self.name_widget = st.empty()
        with col2:
            self.score_widget = st.empty()
    
    def render(self, name: str, score: int):
        self.name_widget.text(name)
        self.score_widget.text(score)


team_2_component = TextTeamScoreComponent()


team_1_component = TextTeamScoreComponent()
team_1_component.render(name="Team 1", score=5)
team_2_component.render(name="Team 2", score=5)
team_2_component.render(name="Team 2", score=15)