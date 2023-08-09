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
    cli_interactor.run()

    workflows.display_approved_registrants_contact_info.assert_called_once_with(
        users_input, presenter=presenter
    )


def test_argparse_cli_adapter():
    cli = ArgparseCLI()
    assert hasattr(cli, "get_input")

    cli.parser = Mock()
    cli.parser.parse_args.return_value = Namespace(workshop_id=1)

    expected_outcome = 1
    observed_outcome = cli.get_input()
    cli.parser.parse_args.assert_called_once()
    assert expected_outcome == observed_outcome


def test_cli_interactor_flow_using_argparse_cli():
    cli = ArgparseCLI()
    workshop_id = 1
    cli.parser = Mock()  # skip getting input from the user
    cli.parser.parse_args.return_value = Namespace(workshop_id=workshop_id)

    workflows = Mock(RegistrantsWorkflows)

    presenter = Mock()

    cli_interactor = RegistrantsCLIInteractor(
        cli=cli,
        workflows=workflows,
        presenter=presenter,
    )
    cli_interactor.run()

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
    cli_interactor.run()

    expected_outcome1 = "email2@gmail.com,\n"
    observed_outcome1 = console.print.call_args[0][0]
    assert observed_outcome1 == expected_outcome1

    cli.parser.parse_args.return_value = Namespace(workshop_id="workshop2")
    cli_interactor.run()

    expected_outcome2 = "email1@gmail.com,\nemail2@gmail.com,\n"
    observed_outcome2 = console.print.call_args[0][0]
    assert observed_outcome2 == expected_outcome2
