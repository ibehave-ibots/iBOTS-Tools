from datetime import date, datetime, timedelta
from random import randint, choices, seed
from string import ascii_letters
from textwrap import dedent
from unittest.mock import Mock



from .workflows import CertificateRepo, PlannedWorkshopWorkflow
from .workshop_repo_inmemory import InMemoryWorkshopRepo
from .course_builder_console import ConsoleWorkshopCertificateBuilder
from .certificate_repo_filesystem import Filesystem, FilesystemCertificateRepo

rand_letters = lambda: ''.join(choices(ascii_letters, k=4))
# rand_date = lambda: datetime(year=randint(1900, 2100), month=randint(1, 12), day=randint(1, 28))
    
                               

def test_workflow_make_certificate_goes_end_to_end():
    
    # Given a workshop exists...
    workshop_id = rand_letters()
    given_workshops = [
        {
            'id': workshop_id, 
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
    
    # Setup test environment
    workflow = PlannedWorkshopWorkflow(
        workshop_repo=InMemoryWorkshopRepo(
            workshops=given_workshops
        ),
        certificate_builder=ConsoleWorkshopCertificateBuilder(),
        certificate_repo=FilesystemCertificateRepo(
            (filesystem := Mock(Filesystem))
        ),
    )
    
    # When we ask to make a certificate from that workshop's id...
    workflow.make_workshop_certificate(workshop_id=workshop_id)
    
    # Then a certificate is saved
    assert filesystem.write.call_count == 1
    assert filesystem.write.call_args[1]['path'].name == f'certificate_{workshop_id}.txt'
    
    
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
    
    