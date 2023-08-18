from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import NamedTuple

from scoreboard.score_calculation import RelativeCommitCalculator

@dataclass
class TeamSettings:
    interval: int = 1
    
    def __post_init__(self):
        if self.interval < 1:
            raise ValueError("interval must be positive.")

class TeamState(NamedTuple):
    points: int = 0
    play_sound: bool = False
    active_branch: str = 'main'


def should_play_sound(played_sound_before: bool, interval: int, old_score: int, new_score: int) -> bool:
    return not played_sound_before and new_score // interval > old_score // interval


class ScoreboardView(ABC):

    @abstractmethod
    def update(self, statuses: dict[str, TeamState]) -> None: ...


@dataclass(frozen=True)
class AppModel:
    statuses: dict[str, TeamState] = field(default_factory=dict)
    settings: dict[str, TeamSettings] = field(default_factory=dict)
    reference_branch: str = 'main'

@dataclass
class Application:
    count_commits: RelativeCommitCalculator
    view: ScoreboardView
    model: AppModel = field(default_factory=AppModel)

    def update_points(self) -> None:
        all_points = self.count_commits(
            ref_branch=self.model.reference_branch, 
            target_branches=list(self.model.statuses.keys())
        )
        for team in self.model.statuses:
            old_status = self.model.statuses[team]
            interval = self.model.settings[team].interval    
            points = all_points[team]
            play_sound = should_play_sound(
                played_sound_before=old_status.play_sound,
                interval=interval,
                old_score=old_status.points,
                new_score=points,
            )
            self.model.statuses[team] = TeamState(points=all_points, play_sound=play_sound)
        self.view.update(model=self.model)

