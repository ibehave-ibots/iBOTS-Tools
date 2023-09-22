from pytest import mark
from external.zoom_api.list_registrants import list_registrants



@mark.slow
@mark.parametrize("status,num", [("approved", 2), ("pending", 0), ("denied", 1)])
def test_get_registrants_gets_right_number_of_registrants_from_meeting_id(
    access_token, status, num
):
    # Given a meeting id
    meeting_id = "838 4730 7377"
    

    # When we ask for zoom meeting
    registrants = list_registrants(
        access_token=access_token, meeting_id=meeting_id, status=status
    )

    # THEN
    assert len(registrants) == num
    for registrant in registrants:
        assert hasattr(registrant, "first_name")
        assert hasattr(registrant, "last_name")
        assert hasattr(registrant, "email")
        assert hasattr(registrant, "status")
        assert hasattr(registrant, "registered_on")
        assert hasattr(registrant, "custom_questions")

