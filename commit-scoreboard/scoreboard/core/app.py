from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field

from scoreboard.core import rules

class VersionControlRepo(ABC):
    @abstractmethod
    def count_commits_ahead(self, ref: str, target: str) -> int: ...


@dataclass
class TeamSettings:
    interval: int = 1
    
    def __post_init__(self):
        if self.interval < 1:
            raise ValueError("interval must be positive.")

@dataclass
class TeamState:
    points: int = 0
    play_sound: bool = False




class ScoreboardView(ABC):

    @abstractmethod
    def update(self, model: AppModel) -> None: ...


@dataclass(frozen=False)
class AppModel:
    statuses: dict[str, TeamState] = field(default_factory=lambda: defaultdict(TeamState))
    settings: dict[str, TeamSettings] = field(default_factory=lambda: defaultdict(TeamSettings))
    reference_branch: str = 'main'

@dataclass
class Application:
    vcs_repo: VersionControlRepo
    view: ScoreboardView
    model: AppModel = field(default_factory=AppModel)

    def update_points(self) -> None:
        for team in self.model.statuses:
            old_status = self.model.statuses[team]
            interval = self.model.settings[team].interval    
            points = self.vcs_repo.count_commits_ahead(ref=self.model.reference_branch, target=team)
            
            play_sound = rules.should_play_sound(
                interval=interval,
                old_score=old_status.points,
                new_score=points,
            )
            self.model.statuses[team] = TeamState(points=points, play_sound=play_sound)
        self.show()

    def show(self) -> None:
        self.view.update(model=self.model)