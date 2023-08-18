import git

from .app import VersionControlRepo




class DummyVersionControlRepo(VersionControlRepo):
    def __init__(self, **commits: dict[str, int]) -> None:
        self.branch_commits = commits

    def count_commits_ahead(self, ref: str, target: str) -> int:
        return self.branch_commits[target] - self.branch_commits[ref]
        

class GitVersionControlRepo(VersionControlRepo):
    def __init__(self, git_repository: git.Repo):
        self.git_repository = git_repository

    def count_commits_ahead(self, ref: str, target: str) -> int:
        return len(list(self.git_repository.iter_commits(f"{ref}..{target}")))

