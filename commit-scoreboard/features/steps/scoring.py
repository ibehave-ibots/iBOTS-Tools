from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple
from unittest.mock import Mock
from behave import given, when, then

class VersionControlRepo(ABC):
    @abstractmethod
    def count_commits_ahead(self, ref: str, target: str) -> int: ...

class DummyVersionControlRepo(VersionControlRepo):
    def __init__(self, **commits: dict[str, int]) -> None:
        self.branch_commits = commits

    def count_commits_ahead(self, ref: str, target: str) -> int:
        return self.branch_commits[target] - self.branch_commits[ref]
        

class Score(NamedTuple):
    score: int

class ScoreboardPresenter(ABC):
    @abstractmethod
    def present(self, scores: dict[str, Any]) -> None: ...


@dataclass(frozen=True)
class CalculateScores:
    version_control_repo: VersionControlRepo
    scoreboard: ScoreboardPresenter

    def run(self, ref_branch: str, target_branches: list[str]) -> None:
        target_branch = target_branches[0]
        commits_ahead = self.version_control_repo.count_commits_ahead(ref=ref_branch, target=target_branch)
        scores = {target_branch: Score(score=commits_ahead)}
        self.scoreboard.present(scores=scores)

        
    


@given(u'the {team} branch is {n:d} commits ahead of the reference {ref} branch')
def step_impl(context, team, ref, n):
    branches = {ref: 0, team: n}
    context.vcs = DummyVersionControlRepo(**branches)
    
    

@when(u'the scores are calculated for teams {team} against reference branch {ref}')
def step_impl(context, team, ref):
    context.scoreboard = Mock(ScoreboardPresenter)
    CalculateScores(
        version_control_repo=context.vcs,
        scoreboard= context.scoreboard
    ).run(ref_branch=ref, target_branches=[team])
    


@then(u'{team} is shown to have a score of {x:d}')
def step_impl(context, team, x):
    scoreboard = context.scoreboard.present.call_args[1]
    assert scoreboard['scores'][team].score == x