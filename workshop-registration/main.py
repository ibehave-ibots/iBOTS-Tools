from adapters import PPrintListWorkshopPresenter, PandasListRegistrantPresenter
from app import ListWorkshopsWorkflow, ListRegistrantsWorkflow, App
from adapters.workshoprepo_zoom import ZoomWorkshopRepo 
import os
from dotenv import load_dotenv
from adapters.registrationrepo_zoom import ZoomRegistrationRepo
from external.zoom_api import list_registrants, get_meeting, get_meetings
from external.zoom_api import OAuthGetToken

def create_app(env_file: str = None) -> App:
    load_dotenv(dotenv_path=env_file)
    oauth = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )

    app = App(
        workshop_workflow = ListWorkshopsWorkflow(
            workshop_repo =ZoomWorkshopRepo(
                group_id=os.environ['TEST_GROUP_ID'],
                get_meeting=get_meeting,
                get_meetings=get_meetings,
                oauth_get_token=oauth
            ),
            registration_repo=ZoomRegistrationRepo(
                list_registrants=list_registrants,
                oauth_get_token=oauth
            ),
            presenter=PPrintListWorkshopPresenter(),
        ),
        registrants_workflow= ListRegistrantsWorkflow(
            registration_repo= ZoomRegistrationRepo(
                list_registrants=list_registrants,
                oauth_get_token=oauth
            ), 
            #presenter=ConsoleListRegistrantPresenter(),
            presenter=PandasListRegistrantPresenter(),
        ),
    )
    return app

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workshop Management")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for listing upcoming workshops
    parser_upcoming = subparsers.add_parser("list_upcoming_workshops", help="List upcoming workshops")

    # Subparser for listing registrants
    parser_registrants = subparsers.add_parser("list_registrants", help="List registrants for a specific workshop")
    parser_registrants.add_argument("workshop_id", type=str, help="Workshop ID to list registrants for")
    parser_registrants.add_argument("--status", type=str, default=None, help="Status filter for registrants")

    args = parser.parse_args()

    app = create_app()
    if args.command == "list_upcoming_workshops":
        app.list_upcoming_workshops()
    elif args.command == "list_registrants":
        app.list_registrants(workshop_id=args.workshop_id, status=args.status)

