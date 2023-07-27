

from .workflows import GetPastWorkshopWorkflows, InMemoryWorkshopRepo


def test_workshop_get_main_details():
    workshops = [
        {'id': 'abc',
        'name': 'Intro2Py',
        },
    ]
    
    repo = InMemoryWorkshopRepo(workshops=workshops)
    workflows = GetPastWorkshopWorkflows(workshop_repo=repo)
    observed_workshop = workflows.get_workshop_details(workshop_id='abc')
    assert observed_workshop.name == workshops[0]['name']
    