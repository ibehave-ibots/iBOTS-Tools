from random import choices
from string import ascii_letters
from pathlib import Path
from unittest.mock import Mock
import git

from scoreboard.adapters.vcs_repo_git import GitVersionControlRepo


def make_test_repo(repo_path, branch_commits: list[tuple[str, int]]) -> git.Repo:
    def write_random_line_and_commit():
        letters = ''.join(choices(ascii_letters, k=3))
        filepath.write_text(letters)
        repo.index.add(str(filepath))
        repo.index.commit(letters)
        
    repo = git.Repo.init(path=repo_path)
    filepath = repo_path / 'main.py'
    write_random_line_and_commit()
    for branch, n_commits in branch_commits:
        repo.create_head(branch)
        repo.git.checkout(branch)
        for _ in range(n_commits):
            write_random_line_and_commit()
    
    return repo




def test_the_test_repo(tmp_path: Path):
    repo = make_test_repo(
        repo_path=tmp_path, 
        branch_commits=[('round1', 4), ('team1-round1', 5)]
    )
    assert len(list(repo.iter_commits('main..round1'))) == 4
    assert len(list(repo.iter_commits('round1..team1-round1'))) == 5
    assert len(list(repo.iter_commits())) == 10  # have to include the initial commit for main.


def test_can_count_commits_from_git_repo(tmp_path: Path):
    # Mock the GitRepository
    git_repo = make_test_repo(
        repo_path=tmp_path,
        branch_commits=[('round1', 7), ('team1-round1', 12)]
    )
    repo = GitVersionControlRepo(git_repo)

    result = repo.count_commits_ahead("round1", "team1-round1")
    assert result == 12

