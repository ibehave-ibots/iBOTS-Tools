from base64 import b64encode
import os
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

