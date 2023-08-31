from collections import defaultdict

from app import RegistrationRecord, RegistrationRepo

class InMemoryRegistrationRepo(RegistrationRepo):
    def __init__(self) -> None:
        self.registrations = defaultdict(list)

    def add_registration(self, registration: RegistrationRecord):
        self.registrations[registration.workshop_id].append(registration)

    def get_registrations(self, workshop_id: str):
        return self.registrations[workshop_id]
    
