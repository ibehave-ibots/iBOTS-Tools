import git

from scoreboard.core.app import VersionControlRepo


class GitVersionControlRepo(VersionControlRepo):
    def __init__(self, git_repository: git.Repo):
        self.git_repository = git_repository

    def count_commits_ahead(self, ref: str, target: str) -> int:
        return len(list(self.git_repository.iter_commits(f"{ref}..{target}")))

