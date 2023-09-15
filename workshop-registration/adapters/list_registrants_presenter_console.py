from typing import List
from app import ListRegistrantPresenter, RegistrantSummary

class ConsoleListRegistrantPresenter(ListRegistrantPresenter):
    def show(self, registrants: List[RegistrantSummary]) -> None:
        print("Name, Registered_on, email, status, affiliation")
        for registrant in registrants:
            print('%s, %s, %s, %s, %s' %(
                registrant.name, 
                registrant.registered_on,
                registrant.email,
                registrant.status,
                registrant.group_name, 
                )
            )