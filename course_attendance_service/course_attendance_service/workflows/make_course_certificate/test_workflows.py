from datetime import date, datetime, timedelta
from random import randint, choices, seed
from string import ascii_letters
from textwrap import dedent
from unittest.mock import Mock


from .workflows import PlannedWorkshopWorkflows
from .repo_inmemory import InMemoryWorkshopRepo
from .presenter_console import ConsoleWorkshopCertificatePresenter

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
                'id': "ABCD", 
                'name': "Intro to Python",
                'description': "A fun workshop on Python!",
                'topics': [
                    'What code is.',
                    'Why to code.',
                    'How to code.',
                ],
                'scheduled_start': date(2023, 8, 9),
                'scheduled_end': date(2023, 8, 14),
                'sessions': [
                    {'id': 'aaa', 
                    'scheduled_start': datetime(2023, 8, 9, 9, 30, 00), 
                    'scheduled_end': datetime(2023, 8, 9, 13, 00),
                    }],
                'organizer': 'The iBOTS',
            },
        ]
        repo = InMemoryWorkshopRepo(workshops=given_workshops)
        workflows = PlannedWorkshopWorkflows(workshop_repo=repo)
        
        printer = Mock()
        presenter = ConsoleWorkshopCertificatePresenter(
            printer = printer
        )
        
        workflows.make_workshop_certificate(workshop_id='ABCD', presenter=presenter)
        expected_certificate = dedent("""
            Workshop Certificate: Intro to Python
            Dates: August 9, 2023 - August 14, 2023
            Organizers: The iBOTS
            
            A fun workshop on Python!
            
            Topics Covered:
              - What code is.
              - Why to code.
              - How to code.
        """)
        observed_certificate = printer.call_args[0][0]
        assert observed_certificate == expected_certificate
        
        