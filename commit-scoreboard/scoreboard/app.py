from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import NamedTuple, Protocol
    

class TeamSettings(NamedTuple):
    interval: int = 0
    

class TeamState(NamedTuple):
    points: int = 0
    play_sound: bool = False


def should_play_sound(played_sound_before: bool, interval: int, old_score: int, new_score: int) -> bool:
    return not played_sound_before and new_score // interval > old_score // interval


class ScoreboardView(ABC):

    @abstractmethod
    def update(self, statuses: dict[str, TeamState]) -> None: ...

@dataclass
class Application:
    view: ScoreboardView
    statuses: dict[str, TeamState] = field(default_factory=dict)
    settings: dict[str, TeamSettings] = field(default_factory=dict)
    

    def update_points(self, team: str, points: int) -> None:
        
        old_status = self.statuses[team]
        interval = self.settings[team].interval
        play_sound = should_play_sound(
            played_sound_before=old_status.play_sound,
            interval=interval,
            old_score=old_status.points,
            new_score=points,
        )
        self.statuses[team] = TeamState(points=points, play_sound=play_sound)
        self.view.update(statuses=self.statuses)

