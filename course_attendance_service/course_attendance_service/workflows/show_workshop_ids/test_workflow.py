from datetime import datetime
from random import randint, choices, seed
from string import ascii_letters
from textwrap import dedent
from unittest.mock import Mock



from .core.workflow import ListWorkshopsWorkflows
from .adapters.repo_inmemory import InMemoryWorkshopRepo
from .adapters.console_printer import ConsoleWorkshopListPresenter, Console

rand_letters = lambda: ''.join(choices(ascii_letters, k=4))
rand_date = lambda: datetime(year=randint(1900, 2100), month=randint(1, 12), day=randint(1, 28))
    
                               
def test_list_all_workshops_ids():
    
    given_workshops = [
        {'id': 'AA'}, 
        {'id': 'BB'}, 
        {'id': 'CC'}, 
    ]
    
    repo = InMemoryWorkshopRepo(workshops=given_workshops)
    console = Mock()
    presenter = ConsoleWorkshopListPresenter(console=console)
    
    workflows = ListWorkshopsWorkflows(workshop_repo=repo)
    workflows.show_all_workshops(presenter=presenter)
    workshop_id_text = console.print.call_args[0][0]
    expected_text = dedent("""
    AA
    BB
    CC
    """).lstrip()
    assert workshop_id_text == expected_text
