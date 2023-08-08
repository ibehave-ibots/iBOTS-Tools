
from unittest.mock import Mock
from .cli import RegistrantsCLI, RegistrantsWorkflows

def test_UI_flow():
    users_input = Mock()
    presenter = Mock()

    cli = Mock()
    cli.get_input.return_value = users_input
    workflows = Mock(RegistrantsWorkflows)
    
    interactor = RegistrantsCLI(cli=cli, workflows=workflows, presenter=presenter)
    interactor.run()

    workflows.display_approved_registrants_contact_info.assert_called_once_with(users_input, presenter=presenter)