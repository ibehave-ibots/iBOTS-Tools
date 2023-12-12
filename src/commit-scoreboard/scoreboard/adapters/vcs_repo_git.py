import git

from scoreboard.core.app import VersionControlRepo


class RemoteGitVersionControlRepo(VersionControlRepo):
    def __init__(self, git_repository: git.Repo, remote: str):
        self.git_repository = git_repository
        self.remote = remote

    def count_commits_ahead(self, ref: str, target: str) -> int:
        self.git_repository.git.fetch()
        query = f"{self.remote}/{ref}..{self.remote}/{target}"
        return len(list(self.git_repository.iter_commits(query)))
    
    def count_all_commits_ahead(self, ref: str) -> dict[str, int]:
        self.git_repository.git.fetch()
        rel_refs = [ref.name for ref in self.git_repository.refs if ref.name.startswith(f'{self.remote}/')]
        rel_refs.remove(f'{self.remote}/{ref}')
        all_counts = {}
        for target in rel_refs:
            query = f"{self.remote}/{ref}..{target}"
            name = target.split('/', 1)[1]
            count = len(list(self.git_repository.iter_commits(query)))
            all_counts[name] = count
        return all_counts