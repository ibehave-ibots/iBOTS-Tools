# %%
from typing import List, Union

from .api_zoom import ZoomRestApi, ZoomRegistrantsData
from .workflows import Registrant, RegistrantsRepo


class ZoomRegistrantsRepo(RegistrantsRepo):
    def __init__(self, zoom_api: ZoomRestApi) -> None:
        self.zoom_api = zoom_api
        self.access_token = "TOP-SECRET"

    @staticmethod
    def turn_zoom_registrants_into_standard_form(
        zoom_registrant: ZoomRegistrantsData,
    ) -> Registrant:
        user_id = zoom_registrant["id"]
        name = f"{zoom_registrant['first_name']} {zoom_registrant['last_name']}"
        affiliation = zoom_registrant["custom_questions"][0]["value"]
        email = zoom_registrant["email"]
        status = zoom_registrant["status"]
        registrant = Registrant(
            user_id=user_id,
            name=name,
            affiliation=affiliation,
            email=email,
            status=status,
        )
        return registrant

    def get_list_of_registrants_for_specific_status(
        self,
        workshop_id: Union[str, int],
        status: str,
    ) -> List[Registrant]:
        zoom_registrants = self.zoom_api.get_registrants(
            access_token=self.access_token,
            workshop_id=workshop_id,
            status=status,
        )
        registrants = []
        for zoom_registrant in zoom_registrants:
            registrant = self.turn_zoom_registrants_into_standard_form(zoom_registrant)
            registrants.append(registrant)
        return registrants

    def get_list_of_registrants(self, workshop_id: Union[str, int]) -> List[Registrant]:
        all_registrants = []
        for status in ["approved", "denied", "pending"]:
            registrants = self.get_list_of_registrants_for_specific_status(
                workshop_id=workshop_id, status=status
            )
            if len(registrants) > 0:
                all_registrants.extend(registrants)
        return all_registrants

    def remove_registrant(self):
        raise NotImplementedError

    def add_registrant(self):
        raise NotImplementedError

    def update_registrant_status(self):
        raise NotImplementedError
