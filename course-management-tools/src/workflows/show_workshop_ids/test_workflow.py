from textwrap import dedent
from unittest.mock import Mock

from .core.workflow import ListWorkshopsWorkflows
from .core.workshop_repo import WorkshopRepo
from .adapters.console_printer import ConsoleWorkshopListPresenter
from ..external.console import Console


      
def test_list_all_workshops_ids(workshop_repo: WorkshopRepo):
    workflows = ListWorkshopsWorkflows(workshop_repo=workshop_repo)
    console = Mock(Console)
    
    # When
    workflows.show_all_workshops(presenter=ConsoleWorkshopListPresenter(console=console))
    
    # Then
    workshop_id_text = console.print.call_args[0][0]
    expected_text = dedent("""
    AA
    BB
    CC
    """).lstrip()
    assert workshop_id_text == expected_text


