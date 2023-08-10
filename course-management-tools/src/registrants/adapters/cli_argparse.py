from argparse import ArgumentParser
from ..core.cli import CLI


class ArgparseCLI(CLI):
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "workshop_id", type=str, help="Unique id of a specific workshop."
        )

    def get_input(self):
        args = self.parser.parse_args()
        return args.workshop_id.replace(" ", "")
