from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Literal, TypedDict, Union
import requests

# API to get participant report from Zoom


class ZoomParticipantsReportData(TypedDict):
    status: Literal["in_meeting", "in_waiting_room"]
    name: str
    user_email: str
    join_time: datetime
    leave_time: datetime


class ZoomMeetingData(TypedDict):
    start_time: datetime
    end_time: datetime


class ZoomParticipantsResponseData(TypedDict):
    participants: List[ZoomParticipantsReportData]


class ZoomRestApi:
    def __init__(self, api_server: str = None):
        self.api_server = (
            api_server if api_server is not None else "https://api.zoom.us/v2"
        )

    @staticmethod
    def get_json_from_zoom_request(url, access_token: str, params: Dict = None):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url=url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_registrants(
        self,
        access_token: str,
        workshop_id: Union[str, int],
        status="approved",
        page_size=100,
    ):
        url = self.api_server + f"/meetings/{workshop_id}/registrants"
        params = {"status": status, "page_size": page_size}
        response_json = self.get_json_from_zoom_request(
            url=url, access_token=access_token, params=params
        )
        data: ZoomGetRegistrantsResponseData = response_json
        return data["registrants"]

    @staticmethod
    def get_past_meeting_details(
        access_token: str, meeting_id: str, params: Dict = None
    ) -> ZoomMeetingData:
        url = f"https://api.zoom.us/v2/report/past_meetings/{meeting_id}"
        header = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_zoom_participant_report(
        access_token: str, meeting_id: str, params: Dict = None
    ) -> ZoomParticipantsResponseData:
        url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
        header = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=header, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_meeting(access_token, meeting_id) -> ZoomGetMeetingResponseData:
        response = requests.get(
            url=f"https://api.zoom.us/v2/meetings/{meeting_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomGetMeetingResponseData = response.json()
        return data

    @staticmethod
    def list_scheduled_meetings_of_user(
        access_token, user_id
    ) -> ZoomListMeetingsResponseData:
        response = requests.get(
            url=f"https://api.zoom.us/v2/users/{user_id}/meetings",
            params={"type": "scheduled"},  # , 'from': from_date, 'to': to_date}
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomListMeetingsResponseData = response.json()
        return data

    @staticmethod
    def list_users_in_group(access_token, group_id):
        response = requests.get(
            url=f"https://api.zoom.us/v2/groups/{group_id}/members",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        data: ZoomListMeetingsResponseData = response.json()
        return data


class ZoomGetMeetingResponseData(TypedDict):
    id: Union[int, str]
    topic: str
    start_time: str  # planned start: '%Y-%m-%dT%H:%M:%SZ'
    duration: int  # minutes
    agenda: str
    occurrences: List[ZoomOccurance]


class ZoomOccurance(TypedDict):
    duration: int
    occurance_id: str
    start_time: str  # date-time
    status: str  # Occurence status


class ZoomListMeetingsResponseData(TypedDict):
    meetings: None


class ZoomRegistrantsData(TypedDict):
    id: str
    first_name: str
    last_name: str
    email: str
    address: str
    city: str
    country: str
    zip: Any
    state: str
    phone: Union[str, int]
    industry: str
    org: Any
    job_title: str
    purchasing_time_frame: Any
    role_in_purchase_process: str
    no_of_employee: int
    comments: str
    custom_questions: List[Dict]
    status: Literal["approved", "denied", "pending"]
    create_time: str
    join_url: str


class ZoomGetRegistrantsResponseData(TypedDict):
    page_size: int
    total_records: int
    next_page_token: str
    registrants: List[ZoomRegistrantsData]
