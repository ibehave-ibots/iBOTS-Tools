from typing import Any, Dict, List, Literal, TypedDict, Union
import requests


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
