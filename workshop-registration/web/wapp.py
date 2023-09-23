from __future__ import annotations
from abc import ABC, abstractmethod

from typing import List, NamedTuple, Optional, Literal
from dataclasses import dataclass, field
from unittest.mock import Mock

from app import ListRegistrantPresenter, RegistrantSummary

from app.registrant_workflows import RegistrantWorkflows
from app.list_workshops_workflow import ListWorkshopsWorkflow
from app.registrationrepo import RegistrationRepo

        
        
class App(NamedTuple):
    repo: RegistrationRepo
    
    def list_registrants(self, workshop_id: str, status: Optional[Literal['approved', 'waitlisted', 'rejected']] = None) -> None:
        presenter = Mock(ListRegistrantPresenter)
        workflows = RegistrantWorkflows(
            registration_repo=self.repo,
            presenter=presenter,
        )
        workflows.list_registrants(workshop_id=workshop_id, status = status)
        registrants = presenter.show.call_args[1]['registrants']
        print('app ran')
        return registrants
        regs = [r.to_dict() for r in registrants] 
        self.model.set_data(data=regs)


    def update_registration_status(
        self, 
        workshop_id: str, 
        registration_id: str,
        to_status: Literal['approved','rejected'],
    ) -> RegistrantSummary:
        presenter = Mock(ListRegistrantPresenter)
        workflows = RegistrantWorkflows(
            registration_repo=self.repo,
            presenter=presenter,
        )
        workflows.update_registrant_status(
            workshop_id=workshop_id, 
            registration_id=registration_id,
            to_status=to_status,
        )
        registrant = presenter.show_update.call_args[1]['registrant']
        return registrant
        # self.model.update_registrant_status(id=registrant.id, status=registrant.status)
                                   

