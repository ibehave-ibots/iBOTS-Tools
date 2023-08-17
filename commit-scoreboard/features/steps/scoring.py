from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, NamedTuple
from unittest.mock import Mock
from behave import given, when, then

class VersionControlRepo(ABC):
    @abstractmethod
    def count_commits_ahead(self, ref: str, target: str) -> int: ...

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

        
        

@given(u'the "team-1" branch is 3 commits ahead of the reference "main" branch')
def step_impl(context):

    # Setup
    context.reference_branch = "main"
    vcs = Mock(VersionControlRepo)
    vcs.count_commits_ahead.return_value = 3

    scoreboard = Mock(ScoreboardPresenter)
    context.calculate_scores = CalculateScores(
        version_control_repo=vcs,
        scoreboard=scoreboard
    ).run
    context.scoreboard = scoreboard

@when(u'the scores are calculated for teams "team1"')
def step_impl(context):
    context.calculate_scores(ref_branch="main", target_branches=['team-1'])


@then(u'"team-1" is shown to have a score of 3')
def step_impl(context):
    scoreboard = context.scoreboard.present.call_args[1]
    assert scoreboard['scores']['team-1'].score == 3