from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
import time
from typing import Iterable, List

from scoreboard.core import rules

class VersionControlRepo(ABC):
    
    @abstractmethod
    def count_all_commits_ahead(self, ref: str) -> dict[str, int]: ...


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

    # @abstractmethod
    def init(self, model: AppModel) -> None: ...

    @abstractmethod
    def update(self, model: AppModel) -> None: ...


class SoundSpeaker(ABC):

    @abstractmethod
    def play_teams_sounds(self, teams: list[str]) -> None: ...


@dataclass(frozen=False)
class AppModel:
    statuses: dict[str, TeamState] = field(default_factory=lambda: defaultdict(TeamState))
    settings: dict[str, TeamSettings] = field(default_factory=lambda: defaultdict(TeamSettings))
    reference_branch: str = 'main'
        
    @property
    def team_names(self) -> List[str]:
        return list(self.statuses.keys())

    def add_teams(self, teams: str | list[str], points: int = 0, interval: int = 1) -> None:
        teams = [teams] if isinstance(teams, str) else teams
        for team in teams:
            self.statuses[team] = TeamState(points=points)
            self.settings[team] = TeamSettings(interval=interval)

@dataclass
class Application:
    vcs_repo: VersionControlRepo
    speaker: SoundSpeaker
    view: ScoreboardView
    model: AppModel = field(default_factory=AppModel)


    def update(self) -> None:
        all_points = self.vcs_repo.count_all_commits_ahead(ref=self.model.reference_branch)
        for team in self.model.statuses:
            old_status = self.model.statuses[team]
            interval = self.model.settings[team].interval    
            points = all_points[team]
            
            play_sound = rules.should_play_sound(
                interval=interval,
                old_score=old_status.points,
                new_score=points,
            )
            self.model.statuses[team] = TeamState(points=points, play_sound=play_sound)

        self._show()


    def run_loop(self, interval: int = 1.5) -> None:
        while True:
            self.update()
            time.sleep(interval)


    def _show(self) -> None:
        self.view.update(model=self.model)
        teams_to_play = [team for team, status in self.model.statuses.items() if status.play_sound]
        if teams_to_play:
            self.speaker.play_teams_sounds(teams=teams_to_play)