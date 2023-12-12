from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from .app import AppModel, ScoreboardView


class ComponentScoreboardView(ScoreboardView):

    def __init__(self, component_factory: Type[TeamScoreComponent]) -> None:
        self.team_components: dict[str, Type[TeamScoreComponent]] = None
        self.component_factory = component_factory

    def init(self, model: AppModel) -> None:
        self.team_components = {name: self.component_factory() for name in model.statuses.keys()}

    def update(self, model: AppModel) -> None:
        for team_name, widget in self.team_components.items():
            widget.render(name=team_name, score=model.statuses[team_name].points)



class TeamScoreComponent(ABC):

    @abstractmethod
    def render(self, name: str, score: int) -> None: ...

