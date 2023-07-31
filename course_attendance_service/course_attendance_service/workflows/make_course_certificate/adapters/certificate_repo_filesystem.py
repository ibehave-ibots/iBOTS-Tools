from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..core.certificate_repo import CertificateRepo
from ..core.certificate_builder import WritableData
from ..external.filesystem import Filesystem


@dataclass(frozen=True)
class FilesystemCertificateRepo(CertificateRepo):
    filesystem:  Filesystem
    
    
    def save_certificate(self, workshop_id: str, certificate_file: WritableData):
        self.filesystem.write_text(
            data=certificate_file.data,
            path=Path(f'certificate_{workshop_id}{certificate_file.recommended_extension}'), 
        )
        
        
