from base64 import b64encode
from datetime import datetime
import os
from typing import Any, Dict, List, Union
import requests


def create_access_token():

    # Check if the required environment variables are present
    required_env_vars = ["CLIENT_ID", "CLIENT_SECRET", "ACCOUNT_ID"]
    missing_env_vars = [
        var for var in required_env_vars if var not in os.environ]

    if missing_env_vars:
        raise KeyError(
            f"Missing environment variables: {', '.join(missing_env_vars)}")

    url = 'https://zoom.us/oauth/token'

    auth_code = b64encode(
        f"{os.environ['CLIENT_ID']}:{os.environ['CLIENT_SECRET']}".encode()).decode()
    header = {
        'Host': 'zoom.us',
        'Authorization': f"Basic {auth_code}"
    }

    data = {
        'grant_type': 'account_credentials',
        'account_id': os.environ['ACCOUNT_ID']
    }

    # Send a POST request to the token URL with the necessary headers and parameters
    try:
        response = requests.post(url=url, headers=header, params=data)
        # Raise an exception if the API request was not successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"An error occurred while creating the access token: {str(e)}")


def get_groups(access_token):
    if not access_token:
        raise ValueError("Access token is required.")

    url = f"https://api.zoom.us/v2/groups"
    output = get_json_from_zoom_request(url=url, access_token=access_token)
    return output


def get_group_members(access_token):
    if not access_token:
        raise ValueError("Access token is required.")

    if "GROUP_ID" not in os.environ or not os.environ["GROUP_ID"]:
        raise KeyError("GROUP_ID environment variable is missing or empty.")

    url = f"https://api.zoom.us/v2/groups/{os.environ['GROUP_ID']}/members"

    output = get_json_from_zoom_request(url=url, access_token=access_token)
    return output


def get_meetings_of_member(access_token, user_id, from_date=None, to_date=None):
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    params={'type': 'scheduled', 'from': from_date, 'to': to_date}
    output = get_json_from_zoom_request(url=url, access_token=access_token,params=params)
    return output

def get_participant_report(access_token, meeting_id):
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    output = get_json_from_zoom_request(url=url, access_token=access_token)
    return output


def get_meeting(access_token, meeting_id):
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}"
    output = get_json_from_zoom_request(url=url, access_token=access_token)
    return output


def get_registrants(access_token, meeting_id):
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/registrants"
    output = get_json_from_zoom_request(url=url, access_token=access_token)
    return output


def get_past_meeting_details(access_token, meeting_id):
    url = f"https://api.zoom.us/v2/past_meetings/{meeting_id}/instances"
    output = get_json_from_zoom_request(url=url, access_token=access_token)
    return output


def get_json_from_zoom_request(url: str, access_token: str, params: Dict = None) -> Union[List, Dict]:
    header = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(url, headers=header, params=params)
    response.raise_for_status()
    return response.json()
