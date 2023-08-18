from dataclasses import dataclass
from pprint import pprint
from random import randint
import time

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, ScoreboardView, TeamSettings, TeamState


class ConsoleView(ScoreboardView):
    def update(self, model: AppModel) -> None:
        # print("Reference:", model.reference_branch)
        # print("Settings:")
        # pprint(dict(model.settings))
        # print("Status:")
        pprint(dict(model.statuses))
        # print('')



def run(app: Application) -> None:
    while True:    
        app.vcs_repo.branch_commits['team-1'] += randint(0, 2)
        app.update_points()
        time.sleep(1)


if __name__ == '__main__':

    app = Application(
        view=ConsoleView(),
        model=AppModel(
            settings={
                'team-1': TeamSettings(interval=9),
            },
            statuses={
                'team-1': TeamState(points=0),
            },
            reference_branch='main',
        ),
        vcs_repo=DummyVersionControlRepo(**{'main': 0, 'team-1': 0}),
    )

    run(app)

