import os
from dotenv import load_dotenv
from pytest import fixture, mark
from external.zoom_api.zoom_oauth import OAuthGetToken


@fixture(scope="session")
def access_token():
    load_dotenv()
    oauth = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )
    access_data = oauth.create_access_token()
    return access_data["access_token"]

@fixture(scope='session')
def user_id():
    load_dotenv()
    user_id = os.environ['TEST_USER_ID']
    return user_id

@mark.slow
def test_can_get_token(access_token):
    assert access_token