from argparse import Namespace
from unittest.mock import Mock

from .interactors.cli import RegistrantsCLIInteractor, RegistrantsWorkflows
from .adapters.cli_argparse import ArgparseCLI


def test_cli_interactor_flow():
    cli = Mock()
    users_input = Mock()
    cli.get_input.return_value = users_input

    workflows = Mock(RegistrantsWorkflows)
    presenter = Mock()
    cli_interactor = RegistrantsCLIInteractor(
        cli=cli,
        workflows=workflows,
        presenter=presenter,
    )
    cli_interactor.display_approved_registrants_contact_info()

    workflows.display_approved_registrants_contact_info.assert_called_once_with(
        users_input, presenter=presenter
    )


def test_approved_registrants_contact_info_argparse_cli_adapter_returns_user_input():
    cli = ArgparseCLI()
    cli.parser = Mock()
    workshop_id = "abc"
    cli.parser.parse_args.return_value = Namespace(workshop_id=workshop_id)

    expected_user_input = workshop_id
    observed_user_input = cli.get_input()
    cli.parser.parse_args.assert_called_once()
    assert expected_user_input == observed_user_input


def test_cli_interactor_flow_using_argparse_cli():
    cli = ArgparseCLI()
    workshop_id = "abc"
    cli.parser = Mock()  # skip getting input from the user
    cli.parser.parse_args.return_value = Namespace(workshop_id=workshop_id)

    workflows = Mock(RegistrantsWorkflows)
    presenter = Mock()
    cli_interactor = RegistrantsCLIInteractor(
        cli=cli,
        workflows=workflows,
        presenter=presenter,
    )
    cli_interactor.display_approved_registrants_contact_info()

    workflows.display_approved_registrants_contact_info.assert_called_once_with(
        workshop_id, presenter=presenter
    )


def test_argparse_cli_displays_approved_registrants_contact_info_correctly(
    console, presenter, registration_workflows
):
    cli = ArgparseCLI()
    cli.parser = Mock()  # skip getting input from the user
    cli.parser.parse_args.return_value = Namespace(workshop_id="workshop1")

    cli_interactor = RegistrantsCLIInteractor(
        cli=cli,
        workflows=registration_workflows,
        presenter=presenter,
    )
    cli_interactor.display_approved_registrants_contact_info()

    expected_outcome1 = "email2@gmail.com,\n"
    observed_outcome1 = console.print.call_args[0][0]
    assert observed_outcome1 == expected_outcome1

    cli.parser.parse_args.return_value = Namespace(workshop_id="workshop2")
    cli_interactor.display_approved_registrants_contact_info()

    expected_outcome2 = "email1@gmail.com,\nemail2@gmail.com,\n"
    observed_outcome2 = console.print.call_args[0][0]
    assert observed_outcome2 == expected_outcome2


def test_argument_parser_returns_valid_workshop_id_when_user_inputs_workshop_id_with_spaces():
    # Given user input workshop id with spaces
    cli = ArgparseCLI()
    cli.parser = Mock()  # skip getting input from the user
    cli.parser.parse_args.return_value = Namespace(workshop_id="123 3456 789")

    # When cli is used with this workshop id
    observed_user_input = cli.get_input()
    expected_user_input = "1233456789"

    # Then the workshop id is without spaces
    assert observed_user_input == expected_user_input
