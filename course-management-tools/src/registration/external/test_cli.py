from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Dict
from unittest.mock import Mock

class CLIRepo(ABC):
    @abstractmethod
    def get_user_inputs(self) -> Dict:
        ...

class ArgparseCLIRepo(CLIRepo):
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            "workshop_id", type=int, help="Unique id of a specific workshop."
        )
    
    def get_user_inputs(self) -> Dict:
        args = self.parser.parse_args()
        return vars(args)
  
  
  
  
    
# def test_cli():
#     cli = Mock(ArgparseCLIRepo)
#     cli.get_user_inputs.return_value = vars(Namespace(a=1))
#     user_inputs = cli.get_user_inputs()
#     assert user_inputs == {"a": 1}
