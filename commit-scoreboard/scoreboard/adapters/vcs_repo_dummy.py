from scoreboard.core.app import VersionControlRepo


class DummyVersionControlRepo(VersionControlRepo):
    def __init__(self, **commits: dict[str, int]) -> None:
        self.branch_commits = commits
    
    def count_all_commits_ahead(self, ref: str) -> dict[str, int]:
        all_counts = {}
        for branch, commits in self.branch_commits.items():
            if branch != ref:
                all_counts[branch] = commits - self.branch_commits[ref]
        return all_counts
        
    def make_commits(self, **commits: dict[str, int]) -> None:
        for branch, commits in commits.items():
            self.branch_commits[branch] += commits