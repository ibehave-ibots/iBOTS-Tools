import streamlit as st

from scoreboard.core.scoreboard_view import TeamScoreComponent


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

