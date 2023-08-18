from random import randint
import time

from scoreboard.core.vcs_repos import DummyVersionControlRepo
from scoreboard.core.app import AppModel, Application, TeamSettings, ScoreboardView, TeamState, SoundSpeaker

from scoreboard.adapters.view_console_with_sound import ConsoleWithSoundView

class RealSoundSpeaker(SoundSpeaker):

    def play_team_sound(self, team) -> None:
        pass


def run(app: Application) -> None:
    while True:    
        for team in app.model.statuses:
            app.vcs_repo.branch_commits[team] += randint(0, 2)
        app.update_points()
        time.sleep(1)




app = Application(
    view=ConsoleWithSoundView(),
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
    speaker=RealSoundSpeaker(),
)

run(app)

