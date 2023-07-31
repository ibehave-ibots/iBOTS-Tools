from __future__ import annotations

from dataclasses import dataclass
from functools import singledispatch
from pathlib import Path
from .workflows import CertificateRepo, WritableData


@dataclass(frozen=True)
class FilesystemCertificateRepo(CertificateRepo):
    filesystem:  Filesystem
    
    
    def save_certificate(self, workshop_id: str, certificate_file: WritableData):
        self.filesystem.write(
            data=certificate_file.data,
            path=Path(f'certificate_{workshop_id}{certificate_file.recommended_extension}'), 
        )
        
        
class Filesystem:
    
    @singledispatch
    @staticmethod
    def write(data, path: Path):
        raise NotImplementedError("Code implemented in dispatched functions")
    
    @write.register(bytes)
    @staticmethod
    def _(data: bytes, path: Path):
        path.write_bytes(data=data)
        
        
    @write.register(str)
    @staticmethod
    def write_text(data: str, path: Path):
        path.write_text(data)