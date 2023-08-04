from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Literal, NamedTuple, Union




class WritableData(NamedTuple):
    data: Union[bytes, str]
    recommended_extension: str
    
    @property
    def data_type(self) -> Literal['bytes', 'str']:
        return 'bytes' if isinstance(self.data, bytes)  else 'str'
    
    

class CertificateBuilder(ABC):
    
    @abstractmethod
    def create_certificate_file(self,
        workshop_name: str, 
        workshop_description: str,
        start: date,
        end: date,
        workshop_topics: List[str],
        organizer: str,
    ) -> WritableData:
        ...                
        