from datetime import datetime
from random import randint, choices, seed
from string import ascii_letters


from .core.workflow import PlannedWorkshopWorkflows
from .adapters.repo_inmemory import InMemoryWorkshopRepo

rand_letters = lambda: ''.join(choices(ascii_letters, k=4))
rand_date = lambda: datetime(year=randint(1900, 2100), month=randint(1, 12), day=randint(1, 28))
    
                               
def test_list_all_workshops_ids():
    seed(42)
    
    for _ in range(10):
        given_workshops = [{'id': rand_letters()} for _ in range(randint(0, 10))]
        
        repo = InMemoryWorkshopRepo(workshops=given_workshops)
        workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
        
        workshop_ids = workflows.list_all_workshops()
        assert workshop_ids == {workshop['id'] for workshop in given_workshops}
