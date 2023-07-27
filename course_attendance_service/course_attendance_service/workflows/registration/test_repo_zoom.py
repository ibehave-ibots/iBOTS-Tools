from unittest.mock import Mock

from .api_zoom import ZoomRestApi, ZoomRegistrantsData
from .repo_zoom import ZoomRegistrantsRepo
from .workflows import Registrant


def get_registrants(access_token=None, workshop_id=None, status=None):
    workshops = {
        "abc": {
            "page_size": 30,
            "total_records": 1,
            "next_page_token": "",
            "registrants": {
                "approved": [
                    ZoomRegistrantsData(
                        id="some_random_chars",
                        first_name="Mo",
                        last_name="Bashiri",
                        custom_questions=[{"value": "iBehave"}],
                        email="mo@email.com",
                        status="approved",
                    )
                ],
                "denied": [],
                "pending": [],
            },
        },
    }
    return workshops[workshop_id]["registrants"][status]


def test_repo_can_get_list_of_registrants_from_zoom_api():
    # GIVEN: the zoom api and a workhop
    zoom_api = Mock(ZoomRestApi)
    zoom_api.get_registrants = get_registrants
    workshop_id = "abc"

    repo = ZoomRegistrantsRepo(zoom_api=zoom_api)

    # WHEN: asked for the list of registrants
    observed_registrants = repo.get_list_of_registrants(workshop_id=workshop_id)
    expected_registrants = [
        Registrant(
            user_id="some_random_chars",
            name="Mo Bashiri",
            affiliation="iBehave",
            email="mo@email.com",
            status="approved",
        )
    ]

    # THEN: the correct list of registrants is returned by the repo
    assert observed_registrants == expected_registrants


def test_repo_can_get_correct_number_of_registrants_from_zoom_api():
    # GIVEN: the zoom api and a workhop
    zoom_api = Mock(ZoomRestApi)
    zoom_api.get_registrants = get_registrants
    workshop_id = "abc"

    repo = ZoomRegistrantsRepo(zoom_api=zoom_api)

    # WHEN: asked for the registrants
    registrants = repo.get_list_of_registrants(workshop_id=workshop_id)
    observed_number = len(registrants)
    expected_number = 1

    # THEN: the number of registrants is correct
    assert observed_number == expected_number
