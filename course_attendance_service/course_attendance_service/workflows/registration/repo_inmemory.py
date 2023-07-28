from typing import Dict, Any, List
from .workflows import Registrant, RegistrantsRepo


class InMemoryRegistrantsRepo(RegistrantsRepo):
    def __init__(self, workshops: Dict[Any, List[Registrant]]):
        self.workshops = workshops

    def get_list_of_registrants(self, workshop_id: Any) -> List[Registrant]:
        return self.workshops[workshop_id]
