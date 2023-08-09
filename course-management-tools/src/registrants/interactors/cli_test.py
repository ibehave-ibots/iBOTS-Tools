from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from unittest.mock import Mock
from .cli import RegistrantsCLIInteractor, RegistrantsWorkflows


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


class CLI(ABC):
    @abstractmethod
    def get_input(self):
        ...


class ArgparseCLI(CLI):
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "workshop_id", help="Unique id of a specific workshop."
        )

    def get_input(self):
        args = self.parser.parse_args()
        return args.workshop_id


def test_argparse_cli_adapter():
    cli = ArgparseCLI()
    assert hasattr(cli, "get_input")

    cli.parser = Mock()
    cli.parser.parse_args.return_value = Namespace(workshop_id=1)

    expected_outcome = 1
    observed_outcome = cli.get_input()
    cli.parser.parse_args.assert_called_once()
    assert expected_outcome == observed_outcome
