from datetime import datetime, timedelta
from random import randint, choices, seed
from string import ascii_letters

from .workflows import PlannedWorkshopWorkflows
from .repo_inmemory import InMemoryWorkshopRepo

rand_letters = lambda: ''.join(choices(ascii_letters, k=4))
rand_date = lambda: datetime(year=randint(1900, 2100), month=randint(1, 12), day=randint(1, 28))
    
                               
def test_list_all_workshops_ids():
    seed(42)
    
    for _ in range(10):
        given_workshops = [{'id': rand_letters()} for _ in range(randint(0, 10))]
        
        repo = InMemoryWorkshopRepo(workshops=given_workshops)
        workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
        
        workshop_ids = workflows.list_all_planned_workshops()
        assert workshop_ids == {workshop['id'] for workshop in given_workshops}

    
def test_get_workshop_details():
    seed(42)
    
    for _ in range(3):
        given_workshops = [
            {
                'id': rand_letters(), 
                'name': rand_letters(),
                'description': rand_letters(),
                'planned_start': (s := rand_date()),
                'planned_end': (s + timedelta(days=randint(1, 6))),
                'sessions': [
                    {'id': (sid := rand_letters()), 
                    'planned_start': (s := rand_date()), 
                    'planned_end': s + timedelta(hours=randint(3, 10)),
                    }],
            },
        ]
        repo = InMemoryWorkshopRepo(workshops=given_workshops)
        workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
        
        workshop = workflows.get_planned_workshop_and_session_details(workshop_id=given_workshops[0]['id'])
        assert workshop.name == given_workshops[0]['name']
        assert workshop.description == given_workshops[0]['description']
        assert workshop.planned_start == given_workshops[0]['planned_start']
        assert workshop.planned_end == given_workshops[0]['planned_end']
        given_sessions = given_workshops[0]['sessions']
        
        session = workshop.sessions[0]
        assert session.start == given_sessions[0]['planned_start']
        assert session.end == given_sessions[0]['planned_end']
    