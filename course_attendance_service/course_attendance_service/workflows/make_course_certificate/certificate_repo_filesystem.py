from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from course_attendance_service.course_attendance_service.workflows.make_course_certificate.workflows import CertificateRepo, WritableData


@dataclass(frozen=True)
class FilesystemCertificateRepo(CertificateRepo):
    filesystem:  Filesystem
    
    
    def save_certificate(self, workshop_id: str, certificate_file: WritableData):
        ...
        
        
class Filesystem:
    
    def write_bytes(path: Path, data: bytes):
        path.write_bytes(data=data)
        
    def write_text(path: Path, data: str):
        path.write_text(data)