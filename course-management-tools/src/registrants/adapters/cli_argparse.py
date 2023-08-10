from argparse import ArgumentParser
from typing import Optional, Tuple
from ..core.cli import CLI


class ArgparseCLI(CLI):
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "workshop_id", type=str, nargs="+", help="Unique id of a specific workshop."
        )

    def get_input(self, args: Optional[Tuple] = None):
        args = self.parser.parse_args(args)
        return "".join(args.workshop_id)
