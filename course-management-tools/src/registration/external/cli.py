from argparse import ArgumentParser


class CLI:
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "workshop_id", help="Unique id of a specific workshop."
        )

    def get_workshop_id_from_user(self):
        args = self.parser.parse_args()
        return args.workshop_id
