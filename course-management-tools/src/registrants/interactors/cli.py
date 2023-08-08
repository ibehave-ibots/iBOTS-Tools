from typing import Any, NamedTuple
from ..core.workflows import RegistrantsWorkflows

class RegistrantsCLI(NamedTuple):
    cli: Any
    workflows: RegistrantsWorkflows
    presenter: Any
    
    def run(self):
        user_inputs = self.cli.get_input()
        self.workflows.display_approved_registrants_contact_info(user_inputs, presenter=self.presenter)
