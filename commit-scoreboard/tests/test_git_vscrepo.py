from unittest.mock import Mock
import git

from scoreboard.workflow import VersionControlRepo


class GitVersionControlRepo(VersionControlRepo):
    def __init__(self, git_repository: git.Repo):
        self.git_repository = git_repository

    def count_commits_ahead(self, ref: str, target: str) -> int:
        return len(list(self.git_repository.iter_commits(f"{ref}..{target}")))




def test_can_count_commits_from_git_repo():
    # Mock the GitRepository
    mock_git_repo = Mock(git.Repo)
    mock_git_repo.iter_commits.return_value = iter('A'*5)
    
    repo = GitVersionControlRepo(mock_git_repo)

    result = repo.count_commits_ahead("main", "feature")
    assert result == 5

if __name__ == "__main__":
    test_can_count_commits_from_git_repo()
