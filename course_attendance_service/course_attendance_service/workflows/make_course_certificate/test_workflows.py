from datetime import datetime, timedelta
from random import randint, choices, seed
from string import ascii_letters
from unittest.mock import Mock

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
        
        workshop_ids = workflows.list_all_workshops()
        assert workshop_ids == {workshop['id'] for workshop in given_workshops}

    
def test_get_workshop_details():
    seed(42)
    
    for _ in range(3):
        given_workshops = [
            {
                'id': rand_letters(), 
                'name': rand_letters(),
                'description': rand_letters(),
                'topics': [
                    'What code is.',
                    'Why to code.',
                    'How to code.',
                ],
                'scheduled_start': (s := rand_date()),
                'scheduled_end': (s + timedelta(days=randint(1, 6))),
                'sessions': [
                    {'id': (sid := rand_letters()), 
                    'scheduled_start': (s := rand_date()), 
                    'scheduled_end': s + timedelta(hours=randint(3, 10)),
                    }],
                'organizer': 'The iBOTS',
            },
        ]
        repo = InMemoryWorkshopRepo(workshops=given_workshops)
        workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
        presenter = Mock()
        workflows.make_workshop_certificate(workshop_id=given_workshops[0]['id'], presenter=presenter)
        certificate_details = presenter.present.call_args[1]
        assert certificate_details['workshop_name'] == given_workshops[0]['name']
        assert certificate_details['workshop_description'] == given_workshops[0]['description']
        assert certificate_details['start'] == given_workshops[0]['scheduled_start']
        assert certificate_details['end'] == given_workshops[0]['scheduled_end']
        assert certificate_details['workshop_topics'] == given_workshops[0]['topics']
        assert certificate_details['organizer'] == given_workshops[0]['organizer']
        