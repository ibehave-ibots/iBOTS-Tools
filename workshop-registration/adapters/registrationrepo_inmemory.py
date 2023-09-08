from collections import defaultdict
from typing import Dict, List

from app import RegistrationRecord, RegistrationRepo

class InMemoryRegistrationRepo(RegistrationRepo):
    def __init__(self) -> None:
        self.registrations: Dict[str, List[RegistrationRecord]] = defaultdict(list)

    def add_registration(self, registration: RegistrationRecord):
        self.registrations[registration.workshop_id].append(registration)

    def get_registrations(self, workshop_id: str):
        return self.registrations[workshop_id]
    
