from __future__ import annotations

from typing import List, NamedTuple

from .entities import WorkshopID
from .workshop_repo import WorkshopRepo
from .workshop_list_presenter import WorkshopListPresenter, WorkshopData


class ListWorkshopsWorkflows(NamedTuple):
    workshop_repo: WorkshopRepo
    
    def show_all_workshops(self, presenter: WorkshopListPresenter = None) -> List[WorkshopID]:
        workshops = self.workshop_repo.list_workshops()
        workshops_out = [WorkshopData(id=w_id) for w_id in workshops]
        presenter.show(workshops_out)
    
    
    
    

