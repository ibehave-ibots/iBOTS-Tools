from collections import defaultdict
from typing import Dict, List

from app import RegistrationRecord, RegistrationRepo
from app.registrationrepo import RegistrationRecord

class InMemoryRegistrationRepo(RegistrationRepo):
    def __init__(self) -> None:
        self.registrations: Dict[str, List[RegistrationRecord]] = defaultdict(list)

    def add_registration(self, registration: RegistrationRecord):
        self.registrations[registration.workshop_id].append(registration)

    def get_registrations(self, workshop_id: str):
        return self.registrations[workshop_id]
    
    def get_registrant(self, workshop_id: str, registration_id: str) -> RegistrationRecord:
        for registration in self.get_registrations(workshop_id=workshop_id):
            if registration.id == registration_id:
                return registration
        else:
            raise IndexError("Registration not found")
        
    def update_registration(self, registration: RegistrationRecord) -> None:
        workshop_id = registration.workshop_id
        registrations = self.registrations[workshop_id]
        for idx, orig in enumerate(registrations):
            if orig.id == registration.id:
                self.registrations[workshop_id][idx] = registration
                break
        else:
            raise IndexError("Registration not Found.")


    