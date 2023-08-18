from dataclasses import dataclass
from pprint import pprint
from random import randint
import time

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, ScoreboardView, TeamSettings, TeamState


class ConsoleView(ScoreboardView):
    def update(self, model: AppModel) -> None:
        pprint(dict(model.statuses))


class ConsoleView2(ScoreboardView):
    def __init__(self) -> None:
        self.first_shown = False

    def _show_header(self, model: AppModel):
        line = '|'
        for team, status in model.statuses.items():
            entry = f' {team:<8}|'
            line += entry
        print(line)

    def update(self, model: AppModel) -> None:
        if not self.first_shown:
            self._show_header(model=model)
            self.first_shown = True

        line = '|'
        for team, status in model.statuses.items():
            ding = "*" if status.play_sound else ""
            entry = f' {str(status.points) + ding:<8}|'
            line += entry
        print(line)

        
        

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

