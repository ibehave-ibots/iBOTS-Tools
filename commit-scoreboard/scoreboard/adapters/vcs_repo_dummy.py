from scoreboard.core.app import VersionControlRepo


class DummyVersionControlRepo(VersionControlRepo):
    def __init__(self, **commits: dict[str, int]) -> None:
        self.branch_commits = commits

    def count_commits_ahead(self, ref: str, target: str) -> int:
        return self.branch_commits[target] - self.branch_commits[ref]
        
    def make_commits(self, **commits: dict[str, int]) -> None:
        for branch, commits in commits.items():
            self.branch_commits[branch] += commits