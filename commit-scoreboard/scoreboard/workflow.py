from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple



@dataclass(frozen=True)
class CalculateScores:
    version_control_repo: VersionControlRepo
    scoreboard: ScoreboardPresenter

    def run(self, ref_branch: str, target_branches: list[str]) -> None:
        target_branch = target_branches[0]
        commits_ahead = self.version_control_repo.count_commits_ahead(ref=ref_branch, target=target_branch)
        scores = {target_branch: Score(score=commits_ahead)}
        self.scoreboard.present(scores=scores)

        
    
class VersionControlRepo(ABC):
    @abstractmethod
    def count_commits_ahead(self, ref: str, target: str) -> int: ...

class Score(NamedTuple):
    score: int

class ScoreboardPresenter(ABC):
    @abstractmethod
    def present(self, scores: dict[str, Any]) -> None: ...
