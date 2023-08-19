from unittest.mock import Mock
import git

from scoreboard.adapters.vcs_repo_git import GitVersionControlRepo


def test_can_count_commits_from_git_repo():
    # Mock the GitRepository
    mock_git_repo = Mock(git.Repo)
    mock_git_repo.iter_commits.return_value = iter('A'*5)
    
    repo = GitVersionControlRepo(mock_git_repo)

    result = repo.count_commits_ahead("main", "feature")
    assert result == 5

if __name__ == "__main__":
    test_can_count_commits_from_git_repo()
