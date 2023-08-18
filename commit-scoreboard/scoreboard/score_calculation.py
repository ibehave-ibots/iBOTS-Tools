from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class RelativeCommitCalculator:
    version_control_repo: VersionControlRepo

    def __call__(self, ref_branch: str, target_branches: list[str]) -> None:
        target_branch = target_branches[0]
        commits_ahead = self.version_control_repo.count_commits_ahead(ref=ref_branch, target=target_branch)
        scores = {target_branch: commits_ahead}
        return scores

    
class VersionControlRepo(ABC):
    @abstractmethod
    def count_commits_ahead(self, ref: str, target: str) -> int: ...

