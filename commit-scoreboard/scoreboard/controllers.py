from random import randint
import time

from scoreboard.adapters.vcs_repo_dummy import DummyVersionControlRepo
from scoreboard.core.app import Application


def run_simulation(app: Application, vcs: DummyVersionControlRepo) -> None:
    while True:    
        new_commits = {team: randint(0, 2) for team in app.model.team_names}
        vcs.make_commits(**new_commits)
        app.update()
        time.sleep(1.5)
