from dataclasses import dataclass
from typing import List

from ..core.workshop_list_presenter import WorkshopListPresenter, WorkshopData
from ..external.console import Console

@dataclass(frozen=True)
class ConsoleWorkshopListPresenter(WorkshopListPresenter):
    console: Console
    
    def show(self, workshops: List[WorkshopData]) -> None:
        text = ""
        for workshop in workshops:
            text += f"{workshop.id}\n"
            
        self.console.print(text)