from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from textwrap import dedent
from typing import Callable, List
from .workflows import WorkshopCertificatePresenter


@dataclass(frozen=True)
class ConsoleWorkshopCertificatePresenter(WorkshopCertificatePresenter):
    printer: Callable[[str], None] = print
    
    def present(
        self, 
        workshop_name: str, 
        workshop_description: str, 
        start: date, 
        end: date, 
        workshop_topics: List[str], 
        organizer: str,
    ) -> None:
        
        text = dedent(f"""
            Workshop Certificate: {workshop_name}
            Dates: {start.strftime("%B %-d, %Y")} - {end.strftime("%B %-d, %Y")}
            Organizers: {organizer}
            
            {workshop_description}
            
            Topics Covered:
              - {workshop_topics[0]}
              - {workshop_topics[1]}
              - {workshop_topics[2]}
        """)
        self.printer(text)
        
        
        