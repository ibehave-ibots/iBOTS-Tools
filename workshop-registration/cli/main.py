import sys
from unittest.mock import Mock
sys.path.append('..')

from typing import Optional
from adapters import (
    PPrintListWorkshopPresenter, 
    PandasListRegistrantPresenter,
    )
from app import (
    App,
    ListWorkshopsWorkflow, 
    RegistrantWorkflows, 
    AttendanceWorkflow,
    )
from adapters.workshoprepo_zoom import ZoomWorkshopRepo 
import os
from dotenv import load_dotenv
from adapters import (
    ZoomRegistrationRepo, 
    ZoomAttendanceRepo, 
    SpreadsheetAttendancePresenter,
    PandasAttendancePresenter,
    )
from external.zoom_api import (
    OAuthGetToken, 
    list_registrants, 
    get_meeting, 
    get_meetings, 
    get_attendees,
    )

def create_app(env_file: Optional[str] = None, presenter: str = "option1") -> App:
    load_dotenv(dotenv_path=env_file)
    oauth = OAuthGetToken(
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        account_id=os.environ["ACCOUNT_ID"],
    )

    presenter_types = {
        "option1": SpreadsheetAttendancePresenter,
        "option2": PandasAttendancePresenter,
    }
    attendance_presenter = presenter_types[presenter]()
    
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
        registrant_workflows= RegistrantWorkflows(
            registration_repo= ZoomRegistrationRepo(
                list_registrants=list_registrants,
                oauth_get_token=oauth
            ), 
            #presenter=ConsoleListRegistrantPresenter(),
            presenter=PandasListRegistrantPresenter(),
        ),
        attendance_workflow=AttendanceWorkflow(
            attendance_repo=ZoomAttendanceRepo(
                oauth_get_token=oauth, 
                get_attendees=get_attendees),
            presenter=attendance_presenter,
        )
    )
    return app

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workshop Management")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for listing upcoming workshops
    parser_upcoming = subparsers.add_parser("list_upcoming_workshops", help="List upcoming workshops")
    parser_upcoming.add_argument("--presenter", "-p", type=str, help="Output format:", choices={"option1", "option2"}, default="option1" )

    # Subparser for listing registrants
    parser_registrants = subparsers.add_parser("list_registrants", help="List registrants for a specific workshop")
    parser_registrants.add_argument("workshop_id", type=str, help="Workshop ID to list registrants for")
    parser_registrants.add_argument("--status", type=str, default=None, help="Status filter for registrants")
    parser_registrants.add_argument("--presenter", "-p", type=str, help="Output format:", choices={"option1", "option2"}, default="option1" )


    parser_attendance_summary = subparsers.add_parser("create_attendance_summary", help="Attendance summary for a specific workshop")
    parser_attendance_summary.add_argument("workshop_id", type=str, help="Workshop ID to create attendance summary for")
    parser_attendance_summary.add_argument("--output_filename", "-o", type=str, help="File name for the CSV file to store the attendance summary in")
    parser_attendance_summary.add_argument("--presenter", "-p", type=str, help="Output format:", choices={"option1", "option2"}, default="option1" )
    
    args = parser.parse_args()

    app = create_app(presenter=args.presenter)
    
    if args.command == "list_upcoming_workshops":
        app.list_upcoming_workshops()
    elif args.command == "list_registrants":
        app.list_registrants(workshop_id=args.workshop_id, status=args.status)
    elif args.command == "create_attendance_summary":
        if args.output_filename:
            app.create_attendance_summary(workshop_id=args.workshop_id, output_filename=args.output_filename)
        else:
            app.create_attendance_summary(workshop_id=args.workshop_id)
