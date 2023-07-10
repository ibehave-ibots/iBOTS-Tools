from base64 import b64encode
from datetime import datetime
import os
import requests


def create_access_token():
    """
    Authenticates with the Zoom API using the provided client credentials and returns the JSON response.

    This function sends a POST request to the Zoom API token URL with the necessary headers and parameters
    to obtain an access token for account-level authentication. The client credentials (CLIENT_ID and CLIENT_SECRET)
    and the account ID (ACCOUNT_ID) are retrieved from the environment variables specified in the .env file.

    Returns:
        dict: The JSON response containing the access token and related information.

    Raises:
        KeyError: If any of the required environment variables (CLIENT_ID, CLIENT_SECRET, ACCOUNT_ID) are missing.
        requests.exceptions.RequestException: If an error occurs while making the API request.

    Example:
        response = authenticate_with_zoom_api()
        print(response)
    """

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
    """
    Retrieves details of Zoom groups using the provided access token.

    Args:
        access_token (str): Access token obtained through authentication.

    Returns:
        dict: The JSON response containing the details of Zoom groups.

    Raises:
        ValueError: If the access_token parameter is an empty string or None.
        requests.exceptions.RequestException: If an error occurs while making the API request.

    Example:
        access_token = "your-access-token"
        response = get_groups(access_token)
        print(response)
    """
    if not access_token:
        raise ValueError("Access token is required.")

    url = f"https://api.zoom.us/v2/groups"

    header = {
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=header)
        # Raise an exception if the API request was not successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"An error occurred while retrieving the groups: {str(e)}")


def get_group_members(access_token):
    """
    Retrieves members of a Zoom group using the provided access token.

    Args:
        access_token (str): Access token obtained through authentication.

    Returns:
        dict: The JSON response containing the members of the Zoom group.

    Raises:
        ValueError: If the access_token parameter is an empty string or None.
        KeyError: If the required environment variable (GROUP_ID) is missing.
        requests.exceptions.RequestException: If an error occurs while making the API request.

    Example:
        access_token = "your-access-token"
        response = get_group_members(access_token)
    """
    if not access_token:
        raise ValueError("Access token is required.")

    if "GROUP_ID" not in os.environ or not os.environ["GROUP_ID"]:
        raise KeyError("GROUP_ID environment variable is missing or empty.")

    url = f"https://api.zoom.us/v2/groups/{os.environ['GROUP_ID']}/members"
    header = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(url, headers=header)
    return response.json()


def get_meetings_of_member(access_token, from_date=None, to_date=None):
    """
    Retrieves the meetings of a Zoom member using the provided access token and optional date filters.

    ... function docstring ...

    Args:
        access_token (str): Access token obtained through authentication.
        from_date (str, optional): Start date in the format 'YYYY-MM-DD' to filter meetings. Defaults to None.
        to_date (str, optional): End date in the format 'YYYY-MM-DD' to filter meetings. Defaults to None.

    Returns:
        dict: The JSON response containing the meetings of the Zoom member.

    Raises:
        ValueError: If the access_token parameter is an empty string or None.
        KeyError: If the required environment variable (USER_ID) is missing.
        ValueError: If the from_date or to_date parameter is provided but is not a valid date format.
        requests.exceptions.RequestException: If an error occurs while making the API request.

    Example:
        access_token = "your-access-token"
        response = get_meetings_of_member(access_token, from_date='2023-01-01', to_date='2023-12-31')
    """
    if not access_token:
        raise ValueError("Access token is required.")

    if "USER_ID" not in os.environ or not os.environ["USER_ID"]:
        raise KeyError("USER_ID environment variable is missing or empty.")

    if from_date:
        try:
            datetime.strptime(from_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Invalid from_date format. It should be in 'YYYY-MM-DD' format.")

    if to_date:
        try:
            datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Invalid to_date format. It should be in 'YYYY-MM-DD' format.")

    url = f"https://api.zoom.us/v2/users/{os.environ['USER_ID']}/meetings"
    header = {
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=header, params={
                                'type': 'scheduled', 'from': from_date, 'to': to_date})
        # Raise an exception if the API request was not successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"An error occurred while retrieving the meetings: {str(e)}")


def get_participant_report(access_token, meeting_id):
    url = f"https://api.zoom.us/v2/report/meetings/{meeting_id}/participants"
    header = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(
        url,
        headers=header
    )
    try:
        response = requests.get(url, headers=header)
        # Raise an exception if the API request was not successful
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"An error occurred while retrieving the participant report: {str(e)}")
