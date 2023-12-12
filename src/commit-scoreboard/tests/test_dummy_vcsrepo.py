from scoreboard.adapters.vcs_repo_dummy import DummyVersionControlRepo



def test_can_add_commits_to_dummy_repo():
    repo = DummyVersionControlRepo(main=0, dev=2, feature=1)
    assert repo.count_all_commits_ahead('main')['dev'] == 2
    assert repo.count_all_commits_ahead('main')['feature'] == 1

    repo.make_commits(dev=1)
    assert repo.count_all_commits_ahead('main')['dev'] == 3
    assert repo.count_all_commits_ahead('main')['feature'] == 1
