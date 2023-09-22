from unittest.mock import Mock
from external.zoom_api.get_meeting import get_meeting, Meeting
from external.zoom_api.get_meetings import get_meetings
from external.zoom_api.list_registrants import list_registrants, ZoomRegistrant
from external.zoom_api.update_registration import update_registration
from pytest import mark
import requests


def test_change_zoom_registrant_status_to_approved_from_pending(access_token, user_id):
    #GIVEN
    workshop_id = "860 5777 0725"
    meeting = get_meeting(access_token=access_token, meeting_id=workshop_id )
    assert meeting.topic == "SANDBOX_MEETING"
    new_status = "approved"
    registrant_email = "tn3@gmail.com"
    registrants_before_update = list_registrants(access_token=access_token,
                                   meeting_id=workshop_id,status="pending")
    
    for r in registrants_before_update:
        if r.email == registrant_email:
            registrant = r
            break    
    
    #WHEN
    update_registration(access_token=access_token,
                        meeting_id=workshop_id,
                        registrant=registrant, 
                        new_status=new_status)

    #THEN
    registrants_after_status_change = list_registrants(access_token=access_token,
                                   meeting_id=workshop_id, 
                                   status=new_status)
    for r in registrants_after_status_change:
        if r.email == registrant_email:
            updated_registrant = r
            break
    
    assert updated_registrant.status == new_status

def reset_registrant_status(access_token: str, meeting_id: str, registrant: ZoomRegistrant) -> None:

    #delete registrant
    registrant_id = registrant.id
    response = requests.delete(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants/{registrant_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        )
    response.raise_for_status()

    #add duplicate registrant 
    parameters = registrant._asdict()
    parameters['status'] = 'pending'
    response = requests.post(
        url=f"https://api.zoom.us/v2/meetings/{meeting_id.replace(' ', '')}/registrants",
        headers={"Authorization": f"Bearer {access_token}"},
        json=parameters
        )
    response.raise_for_status()
    

def test_reset_registrant(access_token):
    # GIVEN a workshop id
    workshop_id = "860 5777 0725"

    non_waitlisted_registrants = []
    for status in ["denied", "approved"]:
        registrants = list_registrants(access_token=access_token,
                                        meeting_id=workshop_id,
                                        status=status)
        non_waitlisted_registrants.extend(registrants)    
    
    # WHEN you reset the status of all non-waitlisted registrants
    for non_waitlisted_registrant in non_waitlisted_registrants:
        reset_registrant_status(access_token=access_token, meeting_id=workshop_id, registrant=non_waitlisted_registrant)


    # THEN the non-waitlisted registrants are deleted from the workshop 
    # AND added with the same details except that their status is now waitlisted
    waitlisted_registrants = list_registrants(access_token=access_token,
                                              meeting_id=workshop_id,
                                              status="pending")
    assert len(waitlisted_registrants) == 4