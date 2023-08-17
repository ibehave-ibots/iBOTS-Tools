from dataclasses import dataclass, field
from typing import Protocol
    

@dataclass
class TeamSettings:
    interval: int = 0
    

@dataclass
class TeamState:
    points: int = 0
    play_sound: bool = False


class StateObserver(Protocol):
    def __call__(self, statuses: dict[str, TeamState]): ...


def should_play_sound(played_sound_before: bool, interval: int, old_score: int, new_score: int) -> bool:
    return not played_sound_before and new_score // interval > old_score // interval


@dataclass
class AppState:
    statuses: dict[str, TeamState] = field(default_factory=dict)
    settings: dict[str, TeamSettings] = field(default_factory=dict)
    observers: set[StateObserver] = field(default_factory=set)

    def update_points(self, team: str, points: int) -> None:
        
        old_status = self.statuses[team]
        interval = self.settings[team].interval
        play_sound = should_play_sound(
            played_sound_before=old_status.play_sound,
            interval=interval,
            old_score=old_status.points,
            new_score=points,
        )
        self.statuses[team].points = points
        self.statuses[team].play_sound = play_sound
        self.notify_observers()

    def register_observer(self, observer) -> None:
        self.observers.add(observer)

    def notify_observers(self) -> None:
        for observer in self.observers:
            observer(statuses=self.statuses)

