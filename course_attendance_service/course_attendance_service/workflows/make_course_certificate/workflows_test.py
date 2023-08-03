from datetime import date, datetime
from textwrap import dedent
from unittest.mock import Mock

import pytest

from .core.workflow import PlannedWorkshopWorkflow
from .adapters.workshop_repo_inmemory import InMemoryWorkshopRepo
from .adapters.certificate_builder_console import ConsoleCertificateBuilder
from .adapters.certificate_repo_filesystem import FilesystemCertificateRepo
from .external.filesystem import Filesystem


@pytest.fixture()
def inmemory_workshop_repo() -> InMemoryWorkshopRepo:
    given_workshops = [
        {
            'id': 'ABCD', 
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
    return repo
                               


def test_workflow_make_certificate_goes_end_to_end(inmemory_workshop_repo):
    

    workflow = PlannedWorkshopWorkflow(
        workshop_repo=inmemory_workshop_repo,
        certificate_builder=ConsoleCertificateBuilder(),
        certificate_repo=FilesystemCertificateRepo(
            (filesystem := Mock(Filesystem))
        ),
    )
    
    # When we ask to make a certificate from that workshop's id...
    workflow.make_workshop_certificate(workshop_id='ABCD')
    
    # Then a certificate is saved
    assert filesystem.write_text.call_count == 1
    assert filesystem.write_text.call_args[1]['path'].name == f'certificate_ABCD.txt'
    
    
    # And the certificate contains the workshop's details.
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
    
    
    # observed_certificate = cert_repo.save_certificate.call_args[1]['certificate_file'].data.encode()
    # assert observed_certificate == expected_certificate
    written_certificate = filesystem.write_text.call_args[1]['data']
    assert written_certificate == expected_certificate
    
    