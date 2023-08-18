from pprint import pprint

from scoreboard.core.app import AppModel, ScoreboardView



class ConsoleView(ScoreboardView):
    def update(self, model: AppModel) -> None:
        pprint(dict(model.statuses))

