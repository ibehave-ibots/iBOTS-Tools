from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from textwrap import dedent
from typing import List
from ..core.certificate_builder import WritableData, CertificateBuilder




@dataclass(frozen=True)
class ConsoleCertificateBuilder(CertificateBuilder):
    
    def create_certificate_file(
        self, 
        workshop_name: str, 
        workshop_description: str, 
        start: date, 
        end: date, 
        workshop_topics: List[str], 
        organizer: str,
    ) -> WritableData:
        
        start_date_str = f"{start:%B} {start.day}, {start:%Y}"
        end_date_str = f"{end:%B} {end.day}, {end:%Y}"

        text = dedent(f"""
            Workshop Certificate: {workshop_name}
            Dates: {start_date_str} - {end_date_str}
            Organizers: {organizer}

            {workshop_description}

            Topics Covered:
              - {workshop_topics[0]}
              - {workshop_topics[1]}
              - {workshop_topics[2]}
        """)
        return WritableData(data=text, recommended_extension='.txt')
        
