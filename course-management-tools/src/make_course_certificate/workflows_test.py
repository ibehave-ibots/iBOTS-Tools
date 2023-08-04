from textwrap import dedent
from unittest.mock import Mock


from .core.workflow import PlannedWorkshopWorkflow
from .core.workshop_repo import WorkshopRepo
from .adapters.certificate_builder_console import ConsoleCertificateBuilder
from .adapters.certificate_repo_filesystem import FilesystemCertificateRepo
from ..external.filesystem import Filesystem



def test_workflow_make_certificate_goes_end_to_end(workshop_repo: WorkshopRepo):
    workflow = PlannedWorkshopWorkflow(
        workshop_repo=workshop_repo,
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
    
    
    # And was written to a file.
    written_certificate = filesystem.write_text.call_args[1]['data']
    assert written_certificate == expected_certificate
    
    