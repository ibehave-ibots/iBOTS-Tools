from random import randint
import time

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, TeamSettings, TeamState

from scoreboard.adapters.view_console import ConsoleView2


        

def run(app: Application) -> None:
    while True:    
        for team in app.model.statuses:
            app.vcs_repo.branch_commits[team] += randint(0, 2)
        app.update_points()
        time.sleep(1)


if __name__ == '__main__':

    app = Application(
        view=ConsoleView2(),
        model=AppModel(
            settings={
                'team-1': TeamSettings(interval=6),
                'team-2': TeamSettings(interval=6),
            },
            statuses={
                'team-1': TeamState(points=0),
                'team-2': TeamState(points=0),
            },
            reference_branch='main',
        ),
        vcs_repo=DummyVersionControlRepo(**{'main': 0, 'team-1': 0, 'team-2': 0}),
    )

    run(app)

