from base64 import b64encode
import requests
from typing import NamedTuple

class OAuthGetToken(NamedTuple):
    client_id: str
    client_secret: str
    account_id: str

    def create_access_token(self):

        url = 'https://zoom.us/oauth/token'

        auth_code = b64encode(
            f"{self.client_id}:{self.client_secret}".encode()).decode()
        header = {
            'Host': 'zoom.us',
            'Authorization': f"Basic {auth_code}"
        }

        data = {
            'grant_type': 'account_credentials',
            'account_id': self.account_id
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

