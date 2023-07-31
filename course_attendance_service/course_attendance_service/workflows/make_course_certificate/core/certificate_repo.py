from __future__ import annotations

from abc import ABC, abstractmethod

from .certificate_builder import WritableData


class CertificateRepo(ABC):
    
    @abstractmethod
    def save_certificate(self, workshop_id: str, certificate_file: WritableData): ...
