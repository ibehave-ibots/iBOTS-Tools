from __future__ import absolute_import
from typing import Any, NamedTuple
from unittest.mock import Mock
from ..registration.core.workflows import RegistrationWorkflows

class RegistrantsCLI(NamedTuple):
    cli: Any
    workflows: RegistrationWorkflows
    presenter: Any
    
    def run(self):
        user_inputs = self.cli.get_input()
        self.workflows.display_approved_registrants_contact_info(user_inputs, presenter=self.presenter)

def test_UI_flow():
    users_input = Mock()
    presenter = Mock()

    cli = Mock()
    cli.get_input.return_value = users_input
    workflows = Mock(RegistrationWorkflows)
    
    interactor = RegistrantsCLI(cli=cli, workflows=workflows, presenter=presenter)
    interactor.run()

    workflows.display_approved_registrants_contact_info.assert_called_once_with(users_input, presenter=presenter)
