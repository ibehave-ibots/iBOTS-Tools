from random import choices
from string import ascii_letters
from pathlib import Path
from unittest.mock import Mock
import git

from scoreboard.adapters.vcs_repo_git import GitVersionControlRepo, RemoteGitVersionControlRepo

def write_random_line_and_commit(repo):
        letters = ''.join(choices(ascii_letters, k=3))
        filepath = Path(repo.working_tree_dir) / 'main.py'
        filepath.write_text(letters)
        repo.index.add(str(filepath))
        repo.index.commit(letters)

def make_test_repo(repo_path, branch_commits: list[tuple[str, int]]) -> git.Repo:
    
        
    repo = git.Repo.init(path=repo_path)
    # filepath = repo_path / 'main.py'
    write_random_line_and_commit(repo=repo)
    for branch, n_commits in branch_commits:
        repo.create_head(branch)
        repo.git.checkout(branch)
        for _ in range(n_commits):
            write_random_line_and_commit(repo=repo)
    
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



def test_can_count_commits_after_fetching_remote_data(tmp_path: Path):
    repo = make_test_repo(
        repo_path=tmp_path, 
        branch_commits=[('round1', 2), ('team1-round1', 6), ('team1-round2', 2)]
    )
    repo2 = repo.clone_from(tmp_path / '.git', tmp_path / 'another_repo.git')
    remote_name = 'origin'

    assert len(list(repo2.iter_commits('origin/round1..origin/team1-round1'))) == 6
    assert len(list(repo2.iter_commits('origin/round1..origin/team1-round2'))) == 8

    # Make 3 more commits on the remote
    repo.git.checkout('team1-round1')
    for _ in range(3):
        write_random_line_and_commit(repo=repo)

    # confirm the cloned repo doesn't know yet
    assert len(list(repo2.iter_commits('origin/round1..origin/team1-round1'))) == 6

    # fetch the data, then confirm the cloned repo knows about the new commits.
    repo2.git.fetch()
    assert len(list(repo2.iter_commits('origin/round1..origin/team1-round1'))) == 9

    rel_refs = [ref.name for ref in repo2.refs if ref.name.startswith('origin/')]
    rel_refs.remove('origin/round1')
    all_counts = {}
    for ref in rel_refs:
        all_counts[ref.split('/', 1)[1]] = len(list(repo2.iter_commits(f'origin/round1..{ref}')))
    assert all_counts['team1-round1'] == 9
    assert all_counts['team1-round2'] == 8
    
    
def test_our_repo_can_count_remote_commits(tmp_path: Path):
    repo = make_test_repo(
        repo_path=tmp_path, 
        branch_commits=[('round1', 2), ('team1-round1', 6)],
    )
    repo2 = repo.clone_from(tmp_path / '.git', tmp_path / 'another_repo.git')
    remote_name = 'origin'

    our_repo = RemoteGitVersionControlRepo(git_repository=repo2, remote='origin')
    assert our_repo.count_commits_ahead('round1', 'team1-round1') == 6

    repo.git.checkout('team1-round1')
    for _ in range(5):
        write_random_line_and_commit(repo=repo)

    assert our_repo.count_commits_ahead('round1', 'team1-round1') == 11
     

def test_can_count_commits_after_fetching_remote_data(tmp_path: Path):
    repo = make_test_repo(
        repo_path=tmp_path, 
        branch_commits=[('round1', 2), ('team1-round1', 6), ('team1-round2', 2)]
    )
    repo2 = repo.clone_from(tmp_path / '.git', tmp_path / 'another_repo.git')
    our_repo = RemoteGitVersionControlRepo(git_repository=repo2, remote='origin')
    counts = our_repo.count_all_commits_ahead(ref='round1')
    assert counts['team1-round1'] == 6
    assert counts['team1-round2'] == 8

    # Make 3 more commits on the original remote
    repo.git.checkout('team1-round1')
    for _ in range(3):
        write_random_line_and_commit(repo=repo)


    counts = our_repo.count_all_commits_ahead(ref='round1')
    assert counts['team1-round1'] == 9
    assert counts['team1-round2'] == 8

    
